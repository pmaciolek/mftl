import ell

from constants import LLM_MODEL


@ell.simple(model=LLM_MODEL)
def anonymize_message(message: str):
    """You are a text anonymizer. Replace any mentions of real people and organizations with fictional but equivalent alternatives.
    Keep the same type (e.g. replace a real company with a fictional company, a real person with a fictional person).
    Maintain the other parts of the text without change. If the processing cannot be done, return empty string."""
    return f"{message}"
