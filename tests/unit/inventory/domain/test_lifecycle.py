from sqlalchemy.sql.functions import now
from annexa.inventory.domain.exceptions import InvalidStateTransitionError
from annexa.inventory.domain.value_objects import RiskTier
import uuid
import pytest
from datetime import datetime, UTC

from annexa.inventory.domain.entities import AISystem
from annexa.inventory.domain.value_objects import SystemState
from annexa.shared.domain.ids import SystemId, TenantId, UserId


@pytest.fixture
def dummy_system() -> AISystem:
    return AISystem(
        id=SystemId(uuid.uuid4()),
        tenant_id=TenantId(uuid.uuid4()),
        name="HR Resume Screener",
        description="Uses OpenAI to rank candidates.",
        owner_id=UserId(uuid.uuid4()),
        created_at=datetime.now(UTC)
    )

def test_system_start_in_draft(dummy_system: AISystem) -> None:
    assert dummy_system.state == SystemState.DRAFT
    assert dummy_system.risk_tier == RiskTier.UNCLASSIFIED

def test_submit_for_review(dummy_system: AISystem) -> None:
    now = datetime.now(UTC)

    dummy_system.submit_for_review(now)
    assert dummy_system.state == SystemState.IN_REVIEW

def test_approve_system(dummy_system: AISystem) -> None:
    now = datetime.now(UTC)
    dummy_system.submit_for_review(now)
    dummy_system.approve(RiskTier.HIGH_RISK, now)

    assert dummy_system.state == SystemState.APPROVED
    assert dummy_system.risk_tier == RiskTier.HIGH_RISK

def test_mark_system_stale(dummy_system: AISystem) -> None:
    now = datetime.now(UTC)
    dummy_system.submit_for_review(now)
    dummy_system.approve(RiskTier.HIGH_RISK, now)
    dummy_system.mark_stale(now)

    assert dummy_system.state == SystemState.STALE

def test_stale_system_can_be_resubmitted(dummy_system: AISystem) -> None:
    now = datetime.now(UTC)
    dummy_system.submit_for_review(now)
    dummy_system.approve(RiskTier.HIGH_RISK, now)
    dummy_system.mark_stale(now)

    dummy_system.submit_for_review(now)
    assert dummy_system.state == SystemState.IN_REVIEW

def test_illegal_state_trasition_raises_error(dummy_system: AISystem) -> None:
    now = datetime.now(UTC)

    with pytest.raises(InvalidStateTransitionError) as exc_info:
        dummy_system.approve(RiskTier.HIGH_RISK, now)

    assert exc_info.value.status == 409
    assert "Cannot transition AI System from 'draft' to 'approved'" in exc_info.value.detail
