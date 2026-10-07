from aether_core.service_registry import ServiceRegistry


def test_service_registry_resolves_food_business_to_shared_service():
    service = ServiceRegistry().resolve("I want to open a restaurant", "business")
    assert service is not None
    assert service.id == "food_business_license"
    assert service.department == "Food Safety"
    assert service.template == "restaurant"


def test_service_registry_contains_broad_govos_service_catalog():
    registry = ServiceRegistry()
    ids = {service.id for service in registry.all()}
    assert len(ids) >= 32
    assert {"property_registration", "gst_registration", "passport", "rera_registration", "crop_insurance"} <= ids


def test_service_registry_respects_customer_type():
    registry = ServiceRegistry()
    assert registry.resolve("I need a scholarship", "business") is None
    assert registry.resolve("I need a scholarship", "citizen").id == "scholarship"
