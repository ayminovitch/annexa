from pathlib import Path
import yaml
from pydantic import ValidationError

from annexa.inventory.domain.value_objects import ProviderRole, RiskTier
from annexa.rules.domain.models import Obligation, RulePack
from annexa.shared.domain.exceptions import DomainError


class RulePackValidationError(DomainError):
    def __init__(self, detail: str) -> None:
        super().__init__(
            code="RULEPACK_VALIDATION_ERROR",
            title="Rule Pack Validation Failed.",
            detail=detail,
            status=500
        )

def load_rulepack(path: str) -> RulePack:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return RulePack.model_validate(data)
    except ValidationError as e:
        raise RulePackValidationError(str(e))
    except FileNotFoundError:
        raise RulePackValidationError(f"Rule pack not found at {path}")

def evaluate_obligations(
        role: ProviderRole,
        tier: RiskTier,
        rule_pack: RulePack
) -> list[Obligation]:
    applicable_obligations: list[Obligation] = []

    for obligation in rule_pack.obligations:
        cond = obligation.conditions

        if cond.roles is not None and role not in cond.roles:
            continue

        if cond.risk_tiers is not None and tier not in cond.risk_tiers:
            continue

        applicable_obligations.append(obligation)

    return applicable_obligations
