"""Generate an OpenAPI schema file for distribution."""

import json
from pathlib import Path

from app.main import create_app

OUTPUT_PATH = Path("openapi.json")


def main() -> None:
    app = create_app()
    schema = app.openapi()
    OUTPUT_PATH.write_text(json.dumps(schema, indent=2, ensure_ascii=False))
    print(f"OpenAPI schema exported to {OUTPUT_PATH}")


if __name__ == "__main__":  # pragma: no cover
    main()