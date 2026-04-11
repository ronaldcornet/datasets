import subprocess
import sys
from pathlib import Path

def validate_instances(schema_path: Path, target_class: str, data_dir: Path) -> bool:
    if not data_dir.exists():
        print(f"{data_dir} does not exist, skipping.")
        return True

    ok = True
    for data_file in sorted(data_dir.glob("*.yaml")):
        rel = data_file.relative_to(Path.cwd())
        print(f"Validating {rel} against {schema_path} ({target_class})...")
        cmd = [
            "linkml-validate",
            "--schema", str(schema_path),
            "--target-class", target_class,
            str(data_file),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            ok = False
            print(f"❌ {rel} failed validation:")
            print(result.stdout)
            print(result.stderr)
        else:
            print(f"✅ {rel} is valid.")
    return ok

def main():
    root = Path(__file__).resolve().parents[1]
    all_ok = True

    # Person examples
    all_ok = validate_instances(
        schema_path=root / "schemas" / "person.yaml",
        target_class="Person",
        data_dir=root / "data" / "person",
    ) and all_ok

    if not all_ok:
        print("❌ One or more instance files failed validation.")
        sys.exit(1)

    print("🎉 All instance files are valid.")
    sys.exit(0)

if __name__ == "__main__":
    main()
