from aether_core.understanding import ObjectiveUnderstandingEngine


def test_understanding_resolves_specific_service():
    result = ObjectiveUnderstandingEngine().understand(
        "I need a driving licence",
        "citizen",
        {"country": "India", "state": "Jammu and Kashmir"},
    )
    assert result.service_id == "driving_license"
    assert result.confidence > 0.5
    assert "driving license" in result.matched_keywords or "driving licence" in result.normalized_objective


def test_understanding_does_not_guess_unknown_objective():
    result = ObjectiveUnderstandingEngine().understand(
        "Please help me with something totally outside the catalog",
        "citizen",
        {"country": "India", "state": "Jammu and Kashmir"},
    )
    assert result.service_id is None
    assert result.ambiguous
    assert result.missing_context


def test_catalog_contains_all_mvp_services():
    from aether_core.service_registry import ServiceRegistry
    assert len(ServiceRegistry().all()) == 33
