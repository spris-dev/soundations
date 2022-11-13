import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    sqlite_db_path: str = os.environ["SND_SQLITE_DB_PATH"]
    spotify_client_id: str = os.environ["CLIENT_ID"]
    spotify_client_secret: str = os.environ["CLIENT_SECRET"]

    sounds_storage_path = "dataset.csv"
    tracks_number_for_genre = 1000
    spoify_limit = 50
