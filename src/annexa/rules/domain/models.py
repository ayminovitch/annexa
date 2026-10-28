from datetime import date
from pydantic import BaseModel, ConfigDict
from annexa.inventory.domain.value_objects import ProviderRole, RiskTier


class Condition(BaseModel):
    roles: list[ProviderRole] | None = None
    risk_tiers: list[RiskTier] | None = None

    model_config = ConfigDict(extra="forbid")

class Obligation(BaseModel):
    id: str
    title: str
    article: str
    deadline: date
    conditions: Condition

    model_config = ConfigDict(extra="forbid")

class RulePack(BaseModel):
    version: str
    description: str
    obligations: list[Obligation]

    model_config = ConfigDict(extra="forbid")
