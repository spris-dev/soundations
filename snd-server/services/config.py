import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    sqlite_db_path: str = os.environ["SND_SQLITE_DB_PATH"]
    spotify_client_id: str = os.environ["SND_SPOTIFY_CLIENT_ID"]
    spotify_client_secret: str = os.environ["SND_SPOTIFY_CLIENT_SECRET"]
    archive_storage_path: str = os.environ["SND_RECOMMENDER_ARCHIVE_PATH"]

    snd_secret_key: str = os.environ["SND_SECRET_KEY"]
    algorithm: str = os.environ["ALGORITHM"]
    access_token_expire_minutes: float = 30

    sounds_storage_path: str = "../data/dataset.csv"
    transformed_sounds_storage_path: str = "../data/transformed_dataset.csv"
    artists_storage_path: str = "../data/artists.csv"
    scaler_storage_path: str = "../data/sc.joblib"

    items_per_search = 1000
    spotify_limit = 50
