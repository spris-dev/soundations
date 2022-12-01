import argparse
import json
from fastapi.openapi.utils import get_openapi

from spotify_crawler import SpotifyCrawler
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
    crawl_tracks_parser = subparsers.add_parser(
        "crawl-tracks", help="Crawls tracks from Spotify API"
    )
    crawl_tracks_parser.add_argument(
        "--resume",
        action="store_true",
        help="Start crawling from the point where you stopped",
    )

    args = parser.parse_args()

    match args.parser_name:
        case "generate-open-api":
            generate_open_api(args)
        case "crawl-tracks":
            crawl_tracks(args)


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


def crawl_tracks(args: argparse.Namespace):
    spotify_crawler = SpotifyCrawler(ctx, args.resume)
    spotify_crawler.set_access_token()

    genres = [
        "alt-rock",
        "alternative",
        "black-metal",
        "death-metal",
        "emo",
        "grunge",
        "hard-rock",
        "hardcore",
        "heavy-metal",
        "j-rock",
        "metal",
        "metal-misc",
        "metalcore",
        "psych-rock",
        "punk",
        "punk-rock",
        "rock",
        "rock-n-roll",
        "rockabilly",
        "classical",
        "hip-hop",
        "indie-pop",
        "drum-and-bass",
        "indie-pop",
    ]

    spotify_crawler.store_dataset_by_genres(genres)


if __name__ == "__main__":
    main()
