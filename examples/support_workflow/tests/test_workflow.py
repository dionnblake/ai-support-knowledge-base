"""Acceptance tests for the isolated synthetic support workflow."""
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from examples.support_workflow.workflow import Workflow

TICKET = {"event_id": "evt-001", "ticket_id": "ticket-001", "subject": "Login access", "body": "My password reset link expired."}
DOCS = [{"source": "access-guide.txt", "text": "For an expired password reset link, request a new reset link. Never share your password."}]

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix=".test-", dir=Path(__file__).resolve().parents[1])
        self.database = Path(self.directory.name) / "sample.sqlite3"
        self.workflow = Workflow(self.database, DOCS)

    def tearDown(self):
        self.workflow.close()
        self.directory.cleanup()

    def test_success_prepares_cited_suggestion_for_review(self):
        result = self.workflow.process(TICKET)
        self.assertEqual(result["state"], "REVIEW_REQUIRED")
        self.assertEqual(result["queue"], "Access support")
        self.assertIn("[1]", result["suggestion"])
        self.assertEqual(result["sources"][0]["source_name"], "access-guide.txt")
        self.assertEqual(result["outbound_actions"], 0)

    def test_duplicate_is_idempotent_across_restarts(self):
        first = self.workflow.process(TICKET)
        self.workflow.close()
        self.workflow = Workflow(self.database, DOCS)
        self.assertEqual(first, self.workflow.process(TICKET))
        with closing(sqlite3.connect(self.database)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM events").fetchone()[0], 1)

    def test_duplicate_id_with_changed_payload_is_rejected(self):
        self.workflow.process(TICKET)
        with self.assertRaisesRegex(ValueError, "different payload"):
            self.workflow.process({**TICKET, "body": "Changed ticket"})

    def test_missing_documentation_suppresses_suggestion(self):
        result = self.workflow.process({**TICKET, "body": "quantum teleportation", "subject": "unrelated"})
        self.assertEqual(result["state"], "MISSING_DOCUMENTATION")
        self.assertIsNone(result["suggestion"])
        with self.assertRaisesRegex(ValueError, "reviewable"):
            self.workflow.review(TICKET["event_id"], True, "Sample reviewer")

    def test_invalid_input_produces_no_event(self):
        for ticket in (None, {}, {**TICKET, "event_id": ""}, {**TICKET, "body": 7}, {**TICKET, "body": "x" * 10001}):
            with self.subTest(ticket=type(ticket).__name__):
                with self.assertRaises(ValueError):
                    self.workflow.process(ticket)
        with closing(sqlite3.connect(self.database)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM events").fetchone()[0], 0)

    def test_simulated_timeout_is_retryable(self):
        result = self.workflow.process(TICKET, simulate_timeout=True)
        self.assertEqual(result["state"], "RETRY_REQUIRED")
        self.assertEqual(result["outbound_actions"], 0)
        self.assertEqual(self.workflow.process(TICKET)["state"], "REVIEW_REQUIRED")

    def test_interruption_recovers_from_durable_checkpoint(self):
        with self.assertRaisesRegex(RuntimeError, "simulated interruption"):
            self.workflow.process(TICKET, interrupt_after_receive=True)
        self.workflow.close()
        self.workflow = Workflow(self.database, DOCS)
        self.assertEqual(self.workflow.process(TICKET)["state"], "REVIEW_REQUIRED")

    def test_review_is_explicit_local_and_terminal(self):
        pending = self.workflow.process(TICKET)
        self.assertEqual(pending["outbound_actions"], 0)
        with self.assertRaises(ValueError):
            self.workflow.review(TICKET["event_id"], True, "")
        with self.assertRaises(ValueError):
            self.workflow.review(TICKET["event_id"], "yes", "Reviewer")
        approved = self.workflow.review(TICKET["event_id"], True, "Sample reviewer")
        self.assertEqual(approved["state"], "APPROVED_LOCAL_ONLY")
        self.assertEqual(approved["outbound_actions"], 0)
        self.assertEqual(approved, self.workflow.process(TICKET))
        with self.assertRaisesRegex(ValueError, "terminal"):
            self.workflow.review(TICKET["event_id"], False, "Sample reviewer")

    def test_rejection_records_outcome_without_outbound_action(self):
        self.workflow.process(TICKET)
        result = self.workflow.review(TICKET["event_id"], False, "Sample reviewer")
        self.assertEqual(result["state"], "REJECTED")
        self.assertEqual(result["outbound_actions"], 0)

if __name__ == "__main__":
    unittest.main()
