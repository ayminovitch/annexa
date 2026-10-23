from enum import StrEnum


class SystemState(StrEnum):
    """Lifecycle states machine for AI Systems."""

    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    STALE = "stale"
    RETIRED = "retired"


class ProviderRole(StrEnum):
    """The organization's legal role under the AI Act for this system."""

    PROVIDER = "provider"
    DEPLOYER = "deployer"
    IMPORTER = "importer"
    DISTRIBUTOR = "distributor"
    NOT_APPLICABLE = "not_applicable"


class RiskTier(StrEnum):
    """The finalized AI Act risk classification."""

    UNCLASSIFIED = "unclassified"
    MINIMAL_RISK = "minimal_risk"
    TRANSPARENCY_RISK = "transparency_risk"
    HIGH_RISK = "high_risk"
    PROHIBITED = "proHIBITED"
    PROHIBITED_PRACTICE = "prohibited_practice"
    GPAI_MODEL = "gpai_model"
