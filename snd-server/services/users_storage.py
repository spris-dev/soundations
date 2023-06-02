from databases import Database
from sqlite3 import IntegrityError

from context import Context
from models.users import UserInDB


class UsersStorage:
    def __init__(self, ctx: Context):
        self.db = Database(f"sqlite+aiosqlite:{ctx.config.sqlite_db_path}")

    async def get_user(self, username: str) -> UserInDB | None:
        query = "SELECT * FROM users WHERE username = :username"
        record = await self.db.fetch_one(query=query, values={"username": username})
        if not record:
            return None

        return UserInDB.parse_obj(record._mapping)

    async def get_user_id(self, username: str) -> int | None:
        query = "SELECT * FROM users WHERE username = :username"
        record = await self.db.fetch_one(query=query, values={"username": username})
        if not record:
            return None

        return record[0]

    async def store_user(self, user: UserInDB) -> UserInDB | None:
        query = "INSERT INTO users(username, hashed_password) VALUES (:username, :hashed_password)"
        try:
            await self.db.execute(query=query, values=user.__dict__)
        except IntegrityError:
            return None

        return await self.get_user(user.username)
