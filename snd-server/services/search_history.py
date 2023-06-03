from databases import Database
from sqlite3 import IntegrityError

from context import Context
from models.users import UserInDB


class SearchHistory:
    def __init__(self, ctx: Context):
        self.db = Database(f"sqlite+aiosqlite:{ctx.config.sqlite_db_path}")
        self.ctx = ctx

    async def store_track(self, user: UserInDB, track_id: str):
        query = (
            "INSERT INTO search_history(track_id, user_id) VALUES (:track_id, :user_id)"
        )
        search_history_track = {"track_id": track_id, "user_id": user.id}
        try:
            await self.db.execute(query=query, values=search_history_track)
        except IntegrityError:
            return None

    async def get_search_history(self, user: UserInDB) -> list[str] | None:
        query = "SELECT track_id FROM search_history WHERE user_id = :user_id"
        records = await self.db.fetch_all(query=query, values={"user_id": user.id})
        if not records:
            return None

        return [record[0] for record in records]
