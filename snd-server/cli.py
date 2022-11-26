import argparse
import json
from fastapi.openapi.utils import get_openapi


from app import create_ctx, create_app

ctx = create_ctx()
app = create_app(ctx)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="parser_name", help="sub-command help")

    generate_open_api_parser = subparsers.add_parser(
        "generate-open-api", help="Generates Open API spec for snd-server"
    )
    generate_open_api_parser.add_argument(
        "--out", type=str, required=True, help="Output path for spec file"
    )

    args = parser.parse_args()

    match args.parser_name:
        case "generate-open-api":
            generate_open_api(args)


def generate_open_api(args: argparse.Namespace):
    with open(args.out, "w") as file:
        json.dump(
            get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
            ),
            file,
        )


if __name__ == "__main__":
    main()
