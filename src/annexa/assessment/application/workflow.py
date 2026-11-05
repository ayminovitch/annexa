from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from annexa.assessment.domain.state import AssessmentState
from annexa.inventory.domain.value_objects import ProviderRole, RiskTier

def ai_screening_node(state: AssessmentState) -> dict[str, str]:
    desc = state.get("description", "").lower()

    if "biometric" in desc:
        return {
            "risk_tier": RiskTier.HIGH_RISK,
            "role": ProviderRole.PROVIDER,
            "justification": "Biometric categorization (Annex III)"
        }

    return {
        "risk_tier": RiskTier.MINIMAL_RISK,
        "role": ProviderRole.DEPLOYER,
        "justification": "General software"
    }

def human_review_node(state: AssessmentState) -> dict[str, str]:
    return {}

def build_assessment_graph() -> StateGraph[AssessmentState]:
    builder = StateGraph(AssessmentState)

    builder.add_node("screen", ai_screening_node)
    builder.add_node("human_review", human_review_node)

    builder.add_edge(START, "screen")
    builder.add_edge("screen", "human_review")
    builder.add_edge("human_review", END)

    return builder
