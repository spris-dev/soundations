import logging
from pathlib import Path
from databases import Database

from context import Context

logger = logging.getLogger(__name__)


class SqliteStorage:
    db: Database

    def __init__(self, ctx: Context):
        self.db = Database(f"sqlite+aiosqlite:{ctx.config.sqlite_db_path}")

    async def connect(self) -> None:
        await self.db.connect()

    async def disconnect(self) -> None:
        await self.db.disconnect()

    async def migrate(self) -> None:
        migrations_folder = Path(Path(__file__).parent, "..", "migrations")
        migrations = sorted(migrations_folder.iterdir())

        async with self.db.transaction():
            for migration in migrations:
                logger.info(f"Running migration {migration}")

                await self.db.execute(query=migration.read_text())
