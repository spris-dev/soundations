import os

class Config:
  sqlite_db_path: str = os.environ["SND_SQLITE_DB_PATH"]
