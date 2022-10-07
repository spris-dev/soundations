import sqlite3
from pathlib import Path

from context import Context

class SqliteStorage:
  def __init__(self, ctx: Context) -> None:
    self.connection = sqlite3.connect(ctx.config.sqlite_db_path)

    run_migrations(self.connection)


def run_migrations(con: sqlite3.Connection) -> None:
  migrations_folder = Path(Path(__file__).parent, '..', 'migrations')
  migrations = sorted(migrations_folder.iterdir())

  with con:
    for migration in migrations:
      print(f"Running migration {migration}")
      con.execute(migration.read_text())
