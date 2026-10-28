from pathlib import Path
from annexa.inventory.domain.value_objects import ProviderRole, RiskTier
from annexa.rules.application.engine import load_rulepack, evaluate_obligations

def test_load_and_evaluate_real_rulepack() -> None:
    rulepack_path = Path("rulepacks/ai_act_omnibus_2026.yaml")
    rulepack = load_rulepack(str(rulepack_path))

    assert rulepack.version == "2026.1.0"
    assert len(rulepack.obligations) == 3

    # test scenario: we are a high risk provider
    obligations = evaluate_obligations(ProviderRole.PROVIDER, RiskTier.HIGH_RISK, rulepack)

    assert len(obligations) == 1
    assert obligations[0].id == "OBL-003"
    assert obligations[0].title == "Establish Quality Management System (Annex III)"

    # test scenario: we are a GPAI provider
    gpai_obs = evaluate_obligations(ProviderRole.PROVIDER, RiskTier.GPAI_MODEL, rulepack)
    assert len(gpai_obs) == 1
    assert gpai_obs[0].id == "OBL-002"

    # test scenario: we are a minimal risk Deployer
    minimal_obs = evaluate_obligations(ProviderRole.DEPLOYER, RiskTier.MINIMAL_RISK, rulepack)
    assert len(minimal_obs) == 0
