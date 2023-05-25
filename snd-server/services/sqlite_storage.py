import logging
from pathlib import Path
from databases import Database

from context import Context
from models.users import UserInDB

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

    async def get_user(self, username) -> UserInDB | None:
        query = "SELECT * FROM users WHERE username = :username"
        record = await self.db.fetch_one(query=query, values={"username": username})
        if not record:
            return None

        return UserInDB.parse_obj(record._mapping)

    async def store_user(self, user) -> UserInDB | None:
        user_in_DB = await self.get_user(user.username)
        if user_in_DB:
            return None

        query = "INSERT INTO users(username, email, hashed_password) VALUES (:username, :email, :hashed_password)"
        await self.db.execute(query=query, values=user.__dict__)

        return await self.get_user(user.username)
