import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    sqlite_db_path: str = os.environ["SND_SQLITE_DB_PATH"]
    spotify_client_id: str = os.environ["SND_SPOTIFY_CLIENT_ID"]
    spotify_client_secret: str = os.environ["SND_SPOTIFY_CLIENT_SECRET"]

    sounds_storage_path = "data/dataset.csv"
    transformed_sounds_storage_path = "data/transformed_dataset.csv"
    artists_storage_path = "data/artists.csv"
    scaler_storage_path = "data/sc.joblib"

    archive_storage_path = "snd-server/archive.zip"
    items_per_search = 1000
    spotify_limit = 50
