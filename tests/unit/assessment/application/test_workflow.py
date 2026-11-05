from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables.config import RunnableConfig

from annexa.assessment.application.workflow import build_assessment_graph
from annexa.assessment.domain.state import AssessmentState
from annexa.inventory.domain.value_objects import ProviderRole, RiskTier


def test_human_in_the_loop_interrupt() -> None:
    builder = build_assessment_graph()
    checkpointer = MemorySaver()
    graph = builder.compile(checkpointer=checkpointer, interrupt_before=["human_review"])

    thread: RunnableConfig = {"configurable": {"thread_id": "assessment-123"}}

    initial_state: AssessmentState = {
        "system_id": "sys-123",
        "description": "AI biometric identification in public spaces."
    }

    for _event in graph.stream(initial_state, thread):
        pass

    state = graph.get_state(thread)
    assert state.next == ("human_review",)

    assert state.values["risk_tier"] == RiskTier.HIGH_RISK

    graph.update_state(
        thread,
        {
            "risk_tier": RiskTier.PROHIBITED_PRACTICE,
            "justification": "Overridden by DPO: Real-time biometric in public space is prohibited."
        }
    )

    for _event in graph.stream(None, thread):
        pass

    final_state = graph.get_state(thread)

    assert not final_state.next
    assert final_state.values["risk_tier"] == RiskTier.PROHIBITED_PRACTICE
    assert "Overridden by DPO" in final_state.values["justification"]