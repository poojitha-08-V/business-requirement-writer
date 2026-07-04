import logging
from pathlib import Path

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path("./templates")


def load_templates() -> list[str]:
    """
    Load all .txt template files from the templates/ directory.
    Returns a list of text strings (one per file).
    """
    if not TEMPLATES_DIR.exists():
        logger.warning(f"Templates directory '{TEMPLATES_DIR}' not found — returning defaults.")
        return _default_templates()

    documents = []
    for path in sorted(TEMPLATES_DIR.glob("*.txt")):
        try:
            text = path.read_text(encoding="utf-8").strip()
            if text:
                documents.append(text)
                logger.info(f"Loaded template: {path.name}")
        except Exception as exc:
            logger.warning(f"Could not read {path.name}: {exc}")

    if not documents:
        logger.warning("No .txt files found in templates/ — returning defaults.")
        return _default_templates()

    return documents


def _default_templates() -> list[str]:
    """Fallback in-memory templates so the app still works without template files."""
    return [
        "Functional requirements define the specific behaviour and functions of a system.",
        "Non-functional requirements specify quality attributes such as performance, security, and scalability.",
        "A user story format: As a <role>, I want <feature>, so that <benefit>.",
        "Acceptance criteria are conditions that a software feature must satisfy to be accepted by a stakeholder.",
        "A Business Requirements Document (BRD) outlines the business solution for a project.",
    ]
