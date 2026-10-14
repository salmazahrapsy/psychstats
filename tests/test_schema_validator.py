import pytest
from pipelines.schema_validator import SchemaValidator

@pytest.fixture
def validator():
    return SchemaValidator()

def test_schema_org_valid(validator):
    payload = {
        "@context": "https://schema.org/",
        "@type": "Dataset",
        "name": "Psychometric Trait Study",
        "description": "Validated behavioral construct test.",
        "creator": {"@type": "Person", "name": "Salma Zahra"}
    }
    is_valid, errors = validator.validate_schema_org(payload)
    assert is_valid is True
    assert len(errors) == 0

def test_schema_org_missing_field(validator):
    payload = {"@context": "https://schema.org/", "name": "Incomplete Dataset"}
    is_valid, errors = validator.validate_schema_org(payload)
    assert is_valid is False
    assert any("description" in e for e in errors)

def test_dublin_core_valid(validator):
    payload = {
        "dublin_core": {
            "title": "Anxiety Scale Metrics",
            "creator": "Salma Zahra",
            "identifier": "https://orcid.org/0009-0007-5941-8494",
            "subject": ["Psychology"],
            "description": "Survey item responses.",
            "type": "Dataset"
        }
    }
    is_valid, errors = validator.validate_dublin_core(payload)
    assert is_valid is True
    assert len(errors) == 0

def test_dublin_core_invalid_orcid(validator):
    payload = {
        "dublin_core": {
            "title": "Invalid ID Sample",
            "creator": "Researcher",
            "identifier": "invalid-id-format",
            "subject": ["Psychology"],
            "description": "Data.",
            "type": "Dataset"
        }
    }
    is_valid, errors = validator.validate_dublin_core(payload)
    assert is_valid is False
    assert any("ORCID" in e for e in errors)
