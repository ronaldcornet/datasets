import json
from pathlib import Path

SCHEMA_PATH = Path("web/person.schema.json")
TARGET_CLASS = "Person"  # or "Person" if that is your class name

def main():
    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    # Only add $ref if $defs and TARGET_CLASS exist
    defs = data.get("$defs") or data.get("definitions")
    if not defs or TARGET_CLASS not in defs:
        raise SystemExit(
            f"Could not find {TARGET_CLASS} in $defs/definitions of {SCHEMA_PATH}"
        )

    # Set the root $ref
    data["$ref"] = f"#/$defs/{TARGET_CLASS}"

    SCHEMA_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Updated root $ref in {SCHEMA_PATH} → {TARGET_CLASS}")

if __name__ == "__main__":
    main()
