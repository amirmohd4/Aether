from backend.aether_core.rule_registry import RuleRegistry


def test_jk_fire_rule_maps_to_fire_noc_service():
    registry = RuleRegistry(records=None)
    fire_rules = [rule for rule in registry.for_jurisdiction({"country": "India", "state": "Jammu and Kashmir"}) if rule.rule_id == "JK-FIRE-001"]
    assert len(fire_rules) == 1
    assert fire_rules[0].service_id == "fire_noc"
    assert fire_rules[0].requirement == "fire_safety_details"


def test_rule_registry_does_not_mark_embedded_pack_production_ready_without_effective_dates():
    registry = RuleRegistry(records=None)
    assert registry.pack_metadata()["production_ready"] is False
