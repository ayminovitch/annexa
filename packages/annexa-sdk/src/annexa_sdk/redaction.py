import re
from typing import Protocol


class Redactor(Protocol):
    def redact(self, text: str) -> str: ...


class EmailRedactor:
    def __init__(self) -> None:
        self._pattern = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")

    def redact(self, text: str) -> str:
        return self._pattern.sub("[EMAIL]", text)


class CreditCardRedactor:
    def __init__(self) -> None:
        self._pattern = re.compile(r"\b(?:\d[ -]*?){13,16}\b")

    def redact(self, text: str) -> str:
        return self._pattern.sub("[CREDIT_CARD]", text)


class PIIPipeline:
    def __init__(self, redactors: list[Redactor]) -> None:
        self.redactors = redactors

    def process(self, text: str) -> str:
        redacted_text = text
        for redactor in self.redactors:
            redacted_text = redactor.redact(redacted_text)
        return redacted_text
