import argparse
import json
import sys

import yaml
from fastapi.openapi.utils import get_openapi
from uvicorn.importer import import_from_string

DEFAULTAPP = "app.main:app"

parser = argparse.ArgumentParser(prog="create_openapi.py")
parser.add_argument(
    "--app", help='App import string. Eg. "main:app"', default=DEFAULTAPP
)
parser.add_argument("--app-dir", help="Directory containing the app", default=None)
parser.add_argument(
    "--out", help="Output file ending in .json or .yaml", default="openapi.json"
)

if __name__ == "__main__":
    args = parser.parse_args()

    if args.app_dir is not None:
        print(f"adding {args.app_dir} to sys.path")
        sys.path.insert(0, args.app_dir)

    print(f"importing app from {args.app}")
    app = import_from_string(args.app)
    # openapi = app.openapi()
    # version = openapi.get("openapi", "unknown version")
    openapi = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )

    print(f"writing openapi spec v{app.version}")
    with open(args.out, "w") as f:
        if args.out.endswith(".json"):
            json.dump(openapi, f, indent=2)
        else:
            yaml.dump(openapi, f, sort_keys=False)

    print(f"spec written to {args.out}")
