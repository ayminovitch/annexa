from collections.abc import Generator
from contextlib import contextmanager

from opentelemetry import trace
from opentelemetry.trace import Span

from annexa_sdk.redaction import CreditCardRedactor, EmailRedactor, PIIPipeline

tracer = trace.get_tracer("annexa.sdk")

default_pipeline = PIIPipeline([EmailRedactor(), CreditCardRedactor()])


@contextmanager
def trace_llm_call(
    system_id: str, model: str, prompt: str, pipeline: PIIPipeline = default_pipeline
) -> Generator[Span]:
    """
    Context manager to trace an LLM call, redact PII, and record metrics

    Usage:
        with trace_llm_call("sys-123", "gemini-2.5-flash", user_prompt) as span:
            response = call_llm(user_prompt)
            span.set_attribute("ai.response", response)
    """
    redacted_prompt = pipeline.process(prompt)

    with tracer.start_as_current_span("llm_generation") as span:
        span.set_attribute("ai.system_id", system_id)
        span.set_attribute("ai.model", model)
        span.set_attribute("ai.prompt.redacted", redacted_prompt)

        try:
            yield span
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise
