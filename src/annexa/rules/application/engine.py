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
            title="Rule Pack Validation Failed",
            detail=detail,
            status=500,
        )


def load_rulepack(path: Path) -> RulePack:
    """Loads a YAML file and validates it tightly against our Pydantic models."""
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return RulePack.model_validate(data)

    except ValidationError as e:
        raise RulePackValidationError(str(e)) from e
    except FileNotFoundError as e:
        raise RulePackValidationError(f"Rule pack not found at {path}") from e


def evaluate_obligations(
    role: ProviderRole,
    tier: RiskTier,
    rulepack: RulePack,
) -> list[Obligation]:
    """
    Deterministic Rules Engine.
    Evaluates an AI System's classifications against the Rule Pack.
    """
    applicable_obligations: list[Obligation] = []

    for obligation in rulepack.obligations:
        cond = obligation.conditions

        if cond.roles is not None and role not in cond.roles:
            continue

        if cond.risk_tiers is not None and tier not in cond.risk_tiers:
            continue

        applicable_obligations.append(obligation)

    return applicable_obligations
