import os
import sys
import json
import yaml
from typing import Dict, List, Tuple

class SchemaValidator:
    SCHEMA_ORG_REQUIRED = ["@context", "@type", "name", "description", "creator"]
    DUBLIN_CORE_REQUIRED = ["title", "creator", "identifier", "subject", "description", "type"]

    def validate_schema_org(self, data: Dict) -> Tuple[bool, List[str]]:
        """Validates JSON-LD against Schema.org structural protocol."""
        errors = []
        for field in self.SCHEMA_ORG_REQUIRED:
            if field not in data:
                errors.append(f"Missing required Schema.org property: '{field}'")

        if data.get("@context") != "https://schema.org/":
            errors.append("Schema.org '@context' must be 'https://schema.org/'")

        creator = data.get("creator", {})
        if not isinstance(creator, dict) or not creator.get("name"):
            errors.append("Schema.org 'creator' must be an object with a 'name' property")

        return (len(errors) == 0, errors)

    def validate_dublin_core(self, data: Dict) -> Tuple[bool, List[str]]:
        """Validates YAML metadata against Dublin Core 15-element standard."""
        errors = []
        dc = data.get("dublin_core", data)
        
        for elem in self.DUBLIN_CORE_REQUIRED:
            if elem not in dc:
                errors.append(f"Missing required Dublin Core element: '{elem}'")

        if "identifier" in dc and not str(dc["identifier"]).startswith("https://orcid.org/"):
            errors.append("Dublin Core 'identifier' must reference a valid ORCID URI")

        return (len(errors) == 0, errors)

    def validate_files(self, schema_file: str, dc_file: str) -> bool:
        print(f"=== Stage 03: Metadata Protocol Validation ===")
        all_passed = True

        # Validate Schema.org
        print(f"\n[1] Auditing Schema.org JSON-LD: {schema_file}")
        with open(schema_file, "r", encoding="utf-8") as f:
            schema_data = json.load(f)
        valid_schema, errors_schema = self.validate_schema_org(schema_data)
        if valid_schema:
            print("✓ Schema.org JSON-LD passed validation.")
        else:
            print(f"✗ Schema.org validation failed:\n  " + "\n  ".join(errors_schema))
            all_passed = False

        # Validate Dublin Core
        print(f"\n[2] Auditing Dublin Core YAML: {dc_file}")
        with open(dc_file, "r", encoding="utf-8") as f:
            dc_data = yaml.safe_load(f)
        valid_dc, errors_dc = self.validate_dublin_core(dc_data)
        if valid_dc:
            print("✓ Dublin Core mapping passed validation.")
        else:
            print(f"✗ Dublin Core validation failed:\n  " + "\n  ".join(errors_dc))
            all_passed = False

        return all_passed

if __name__ == "__main__":
    validator = SchemaValidator()
    success = validator.validate_files("config/schema_ld_template.json", "config/dublin_core_mapping.yaml")
    sys.exit(0 if success else 1)
