import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class BaseEntity:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime = field(init=False)

    def __post_init__(self) -> None:
        if not hasattr(self, "updated_at"):
            self.updated_at = self.created_at

    def touch(self, now: datetime) -> None:
        self.updated_at = now
