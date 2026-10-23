from datetime import datetime

from annexa.inventory.domain.exceptions import InvalidStateTransitionError
from annexa.inventory.domain.value_objects import RiskTier
from annexa.inventory.domain.value_objects import ProviderRole
from dataclasses import dataclass, field

from annexa.inventory.domain.value_objects import SystemState
from annexa.shared.domain.entity import BaseEntity
from annexa.shared.domain.ids import SystemId, TenantId, UserId


@dataclass(kw_only=True)
class AISystem(BaseEntity):
    id: SystemId
    tenant_id: TenantId
    name: str
    description: str
    owner_id: UserId

    # Internal state protected from arbitrary mutation
    _state: SystemState = field(default=SystemState.DRAFT)

    # Classification date
    provider_role: ProviderRole = field(default=ProviderRole.NOT_APPLICABLE)
    risk_tier: RiskTier = field(default=RiskTier.UNCLASSIFIED)

    @property
    def state(self) -> SystemState:
        return self._state

    def submit_for_review(self, now: datetime) -> None:
        if self._state not in (SystemState.DRAFT, SystemState.STALE):
            raise InvalidStateTransitionError(self._state.value, SystemState.IN_REVIEW.value)

        self._state = SystemState.IN_REVIEW
        self.touch(now)

    def approve(self, risk_tier: RiskTier, now: datetime) -> None:
        if self._state != SystemState.IN_REVIEW:
            raise InvalidStateTransitionError(self._state.value, SystemState.APPROVED.value)

        self.risk_tier = risk_tier
        self._state = SystemState.APPROVED
        self.touch(now)

    def mark_stale(self, now: datetime) -> None:
        if self._state != SystemState.APPROVED:
            raise InvalidStateTransitionError(self._state.value, SystemState.STALE.value)

        self._state = SystemState.STALE
        self.touch(now)

    def retire(self, now: datetime) -> None:
        if self._state == SystemState.RETIRED:
            raise InvalidStateTransitionError(self._state.value, SystemState.RETIRED.value)

        self._state = SystemState.RETIRED
        self.touch(now)
