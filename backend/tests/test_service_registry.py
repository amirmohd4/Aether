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


def test_revenue_department_catalog_covers_core_land_and_certificate_services():
    registry = ServiceRegistry()
    revenue_services = {
        service.id for service in registry.all() if service.department == "Revenue"
    }
    assert {
        "mutation",
        "land_conversion",
        "title_verification",
        "domicile_certificate",
        "income_certificate",
        "caste_certificate",
        "legal_heir_certificate",
        "certified_land_record",
        "jamabandi_copy",
        "khasra_girdawari_copy",
        "land_partition",
        "land_demarcation",
        "land_record_correction",
        "land_possession_certificate",
        "land_encroachment_complaint",
        "land_acquisition_compensation",
        "revenue_case_status",
        "state_land_lease",
        "disaster_damage_assessment",
    } <= revenue_services


def test_developer_can_resolve_revenue_land_services():
    registry = ServiceRegistry()
    assert registry.resolve("I need a fard / jamabandi copy", "developer").id in {
        "certified_land_record", "jamabandi_copy"
    }
    assert registry.resolve("I need land demarcation for my project", "developer").id == "land_demarcation"
    assert registry.resolve("I need mutation of land ownership", "developer").id == "mutation"
