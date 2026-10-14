"""Run original synthetic tickets through the local-only workflow."""
import json
from pathlib import Path
from examples.support_workflow.workflow import Workflow

DOCUMENTS = [{"source": "access-guide.txt", "text": "For an expired password reset link, request a new reset link. Never share your password."}]
TICKET = {"event_id": "example-001", "ticket_id": "sample-001", "subject": "Login access", "body": "My password reset link expired."}

def main() -> None:
    """Print actual sample results; persist only under this repository's work folder."""
    root = Path(__file__).resolve().parents[2]
    workflow = Workflow(root / "work" / "support-workflow-demo" / "sample.sqlite3", DOCUMENTS)
    try:
        result = workflow.process(TICKET)
        duplicate = workflow.process(TICKET)
        missing = workflow.process({**TICKET, "event_id": "example-002", "subject": "Unrelated", "body": "quasar neutrino oscillations"})
        report = {"mode": "SYNTHETIC_LOCAL_ONLY", "response_type": "DETERMINISTIC_TEMPLATE", "prepared": result, "duplicate_returns_same_result": result == duplicate, "missing_documentation": missing, "human_review": "PENDING", "outbound_actions": 0, "integrations": "NONE: no Zendesk, Salesforce or LLM calls"}
        print(json.dumps(report, indent=2))
    finally:
        workflow.close()

if __name__ == "__main__":
    main()
