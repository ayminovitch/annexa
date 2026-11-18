from collections.abc import Iterator
from contextlib import contextmanager
from typing import Self

import pytest
from opentelemetry.trace import Status, StatusCode

import annexa_sdk.telemetry as telemetry_mod
from annexa_sdk.redaction import CreditCardRedactor, EmailRedactor, PIIPipeline
from annexa_sdk.telemetry import trace_llm_call


class FakeSpan:
    def __init__(self) -> None:
        self.attributes: dict[str, object] = {}
        self.exceptions: list[BaseException] = []
        self.status: Status | None = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        return None

    def set_attribute(self, key: str, value: object) -> None:
        self.attributes[key] = value

    def record_exception(self, exception: BaseException) -> None:
        self.exceptions.append(exception)

    def set_status(self, status: Status) -> None:
        self.status = status


class FakeTracer:
    def __init__(self, span: FakeSpan) -> None:
        self._span = span

    @contextmanager
    def start_as_current_span(self, name: str) -> Iterator[FakeSpan]:
        yield self._span


def test_pii_pipeline_redacts_email_and_credit_card() -> None:
    pipeline = PIIPipeline([EmailRedactor(), CreditCardRedactor()])
    text = "Contact ceo@annexa.eu with card 4111-2222-3333-4444."

    redacted = pipeline.process(text)

    assert redacted == "Contact [EMAIL] with card [CREDIT_CARD]."


def test_trace_llm_call_records_redacted_prompt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_span = FakeSpan()
    monkeypatch.setattr(telemetry_mod, "tracer", FakeTracer(fake_span))

    with trace_llm_call(
        system_id="sys-1",
        model="gemini",
        prompt="Hi, my email is ceo@annexa.eu. Is this AI safe?",
    ) as span:
        span.set_attribute("ai.response", "Yes")

    assert fake_span.attributes["ai.system_id"] == "sys-1"
    assert fake_span.attributes["ai.model"] == "gemini"
    assert (
        fake_span.attributes["ai.prompt.redacted"]
        == "Hi, my email is [EMAIL]. Is this AI safe?"
    )
    assert fake_span.attributes["ai.response"] == "Yes"


def test_trace_llm_call_records_exception_on_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_span = FakeSpan()
    monkeypatch.setattr(telemetry_mod, "tracer", FakeTracer(fake_span))

    with (
        pytest.raises(TimeoutError),
        trace_llm_call(
            system_id="sys-1",
            model="gemini",
            prompt="Hello",
        ),
    ):
        raise TimeoutError("LLM timed out")

    assert len(fake_span.exceptions) == 1
    assert isinstance(fake_span.exceptions[0], TimeoutError)
    assert fake_span.status is not None
    assert fake_span.status.status_code == StatusCode.ERROR
