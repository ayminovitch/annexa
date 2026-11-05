from typing import TypedDict

from annexa.inventory.domain.value_objects import ProviderRole, RiskTier


class AssessmentState(TypedDict, total=False):
    system_id: str
    description: str

    role: ProviderRole
    risk_tier: RiskTier
    justification: str
