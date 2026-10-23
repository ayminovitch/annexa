from annexa.shared.domain.exceptions import DomainError


class InvalidStateTransitionError(DomainError):
    def __init__(self, current_state: str, target_state: str) -> None:
        super().__init__(
            code="INVALID_STATE_TRANSITION",
            title="Invalid State Transition",
            detail=f"Cannot transition AI System from '{current_state}' to '{target_state}'.",
            status=409,
        )
