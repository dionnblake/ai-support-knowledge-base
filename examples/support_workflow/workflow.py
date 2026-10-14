"""Synthetic local support workflow. No network client or outbound action exists."""
import hashlib
import json
import re
import sqlite3
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from app.utils.citation_utils import parse_citations


class Workflow:
    """Persist ticket checkpoints, deterministic suggestions and explicit local review."""

    def __init__(self, database: Path, documents: list[dict[str, str]]) -> None:
        """Open an explicitly supplied sample database; never use app production config."""
        self.database = Path(database)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self.documents = documents
        self.connection = sqlite3.connect(self.database)
        self.connection.execute("PRAGMA synchronous=FULL")
        self.connection.execute("CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, result TEXT NOT NULL)")
        self.connection.commit()

    @staticmethod
    def _validate(ticket: Any) -> dict[str, str]:
        """Reject invalid input before creating any event record."""
        if not isinstance(ticket, dict):
            raise ValueError("Ticket must be an object")
        limits = {"event_id": 80, "ticket_id": 80, "subject": 200, "body": 10000}
        result = {}
        for key, limit in limits.items():
            value = ticket.get(key)
            if not isinstance(value, str) or not value.strip() or len(value) > limit:
                raise ValueError(f"Invalid {key}: nonempty text required, limit {limit}")
            result[key] = value.strip()
        for key in ("event_id", "ticket_id"):
            if not re.fullmatch(r"[A-Za-z0-9_-]+", result[key]):
                raise ValueError(f"Invalid {key}: use letters, digits, underscores or hyphens")
        return result

    def _save(self, event_id: str, fingerprint: str, result: dict[str, Any]) -> None:
        """Commit a complete checkpoint atomically in SQLite."""
        with self.connection:
            self.connection.execute("INSERT INTO events VALUES (?, ?, ?) ON CONFLICT(event_id) DO UPDATE SET result=excluded.result", (event_id, fingerprint, json.dumps(result, sort_keys=True)))

    def process(self, ticket: Any, *, simulate_timeout: bool = False, interrupt_after_receive: bool = False) -> dict[str, Any]:
        """Validate, recommend a queue and prepare a cited deterministic suggestion."""
        normalized = self._validate(ticket)
        event_id = normalized["event_id"]
        fingerprint = hashlib.sha256(json.dumps(normalized, sort_keys=True).encode()).hexdigest()
        row = self.connection.execute("SELECT fingerprint, result FROM events WHERE event_id=?", (event_id,)).fetchone()
        if row:
            if row[0] != fingerprint:
                raise ValueError("Duplicate event ID has a different payload")
            existing = json.loads(row[1])
            if existing["state"] not in ("RECEIVED", "RETRY_REQUIRED"):
                return existing
        result: dict[str, Any] = {"event_id": event_id, "ticket_id": normalized["ticket_id"], "state": "RECEIVED", "mode": "SYNTHETIC_LOCAL_ONLY", "outbound_actions": 0, "suggestion": None, "sources": []}
        self._save(event_id, fingerprint, result)
        if interrupt_after_receive:
            raise RuntimeError("simulated interruption after durable receipt")
        if simulate_timeout:
            result.update(state="RETRY_REQUIRED", reason="Simulated external timeout; no integration was called")
            self._save(event_id, fingerprint, result)
            return result
        query = (normalized["subject"] + " " + normalized["body"]).lower()
        result["queue"] = "Access support" if any(term in query for term in ("login", "password", "reset")) else "General support"
        stopwords = {"a", "an", "the", "my", "i", "is", "it", "to", "for", "of", "and", "in", "on"}
        terms = set(re.findall(r"[a-z0-9]+", query)) - stopwords
        matches = [doc for doc in self.documents if terms.intersection(re.findall(r"[a-z0-9]+", doc["text"].lower()))]
        if not matches:
            result.update(state="MISSING_DOCUMENTATION", reason="No supporting sample document; escalate to a human")
        else:
            documents = [SimpleNamespace(page_content=doc["text"], metadata={"source": Path(doc["source"]).name}) for doc in matches[:2]]
            suggestion = "Draft for human review (deterministic template): " + " ".join(f"{doc.page_content} [{index}]" for index, doc in enumerate(documents, 1))
            suggestion, sources = parse_citations(suggestion, documents)
            result.update(state="REVIEW_REQUIRED", suggestion=suggestion, sources=sources, response_type="DETERMINISTIC_TEMPLATE")
        self._save(event_id, fingerprint, result)
        return result

    def review(self, event_id: str, approved: bool, reviewer: str) -> dict[str, Any]:
        """Record local review only. This API cannot send a message or update a CRM."""
        if type(approved) is not bool or not isinstance(reviewer, str) or not reviewer.strip() or len(reviewer) > 100:
            raise ValueError("Explicit Boolean approval and reviewer name required")
        row = self.connection.execute("SELECT fingerprint, result FROM events WHERE event_id=?", (event_id,)).fetchone()
        if row is None:
            raise ValueError("Event is not reviewable")
        result = json.loads(row[1])
        if result["state"] in ("APPROVED_LOCAL_ONLY", "REJECTED"):
            raise ValueError("Review outcome is terminal")
        if result["state"] != "REVIEW_REQUIRED":
            raise ValueError("Event is not reviewable")
        result.update(state="APPROVED_LOCAL_ONLY" if approved else "REJECTED", reviewer=reviewer.strip(), outcome="Local review recorded; no outbound action")
        self._save(event_id, row[0], result)
        return result

    def close(self) -> None:
        """Release the sample SQLite connection."""
        self.connection.close()
