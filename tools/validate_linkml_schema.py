import json
import os
import sys
from pathlib import Path
from urllib.request import urlopen

import yaml
from jsonschema import Draft202012Validator
from linkml_runtime.utils.schemaview import SchemaView

META_SCHEMA_URL = "https://w3id.org/linkml/meta.schema.json"


def load_meta_schema():
    print(f"Downloading LinkML meta-schema from {META_SCHEMA_URL} ...")
    with urlopen(META_SCHEMA_URL) as resp:
        return json.load(resp)


def validate_with_meta_schema(schema_obj, validator, rel_path):
    errors = sorted(validator.iter_errors(schema_obj), key=lambda e: e.path)
    if errors:
        print(f"❌ {rel_path}: NOT a valid LinkML schema (meta-schema violations):")
        for err in errors:
            path = ".".join(str(p) for p in err.path)
            print(f"   - {path}: {err.message}")
        return False
    else:
        print(f"✅ {rel_path}: passes meta-schema validation")
        return True


def validate_with_schemaview(schema_path, rel_path):
    try:
        SchemaView(str(schema_path))
        print(f"✅ {rel_path}: successfully loaded by SchemaView")
        return True
    except Exception as e:
        print(f"❌ {rel_path}: failed to load with SchemaView")
        print(f"   Error: {e}")
        return False


def main():
    repo_root = Path(__file__).resolve().parents[1]
    schemas_dir = repo_root / "schemas"

    if not schemas_dir.exists():
        print(f"schemas/ directory not found at {schemas_dir}")
        sys.exit(1)

    meta_schema = load_meta_schema()
    validator = Draft202012Validator(meta_schema)

    all_ok = True

    for schema_path in sorted(schemas_dir.glob("*.yaml")):
        rel_path = schema_path.relative_to(repo_root)

        # 1. Load YAML
        try:
            with open(schema_path) as f:
                schema_obj = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ {rel_path}: failed to parse YAML: {e}")
            all_ok = False
            continue

        # 2. Validate against LinkML meta-schema
        ok_meta = validate_with_meta_schema(schema_obj, validator, rel_path)

        # 3. Try loading with SchemaView
        ok_sv = validate_with_schemaview(schema_path, rel_path)

        all_ok = all_ok and ok_meta and ok_sv

    if not all_ok:
        print("❌ One or more schemas are invalid.")
        sys.exit(1)

    print("🎉 All LinkML schemas are valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()
