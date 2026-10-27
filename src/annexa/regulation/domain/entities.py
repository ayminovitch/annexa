from dataclasses import dataclass, field

from annexa.shared.domain.entity import BaseEntity
from annexa.shared.domain.ids import ChunkId

@dataclass(kw_only=True)
class RegulationChunk(BaseEntity):
    id: ChunkId
    regulation_version: str # e.g., "2026/1689"
    article: str | None # e.g., "Article 1"
    paragraph: str | None # e.g., "1(a)"
    text: str
    embedding: list[float] | None = field(default=None)
