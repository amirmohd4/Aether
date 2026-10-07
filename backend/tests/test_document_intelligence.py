from aether_core.document_intelligence import DocumentIntelligence


def test_document_intelligence_extracts_core_fields():
    result = DocumentIntelligence().inspect([
        {"type": "property_record", "text": "Owner: Amir Khan\nParcel ID: JK-12-44\nArea: 2.0 acres"}
    ], ["property_record"])
    assert result["status"] == "complete"
    extracted = result["checks"][0]["extracted"]
    assert extracted["owner_name"] == "Amir Khan"
    assert extracted["parcel_id"] == "JK-12-44"
    assert extracted["area"] == "2.0"


def test_missing_document_is_explicit():
    result = DocumentIntelligence().inspect([], ["identity_document"])
    assert result["status"] == "needs_attention"
    assert result["missing"] == ["identity_document"]
