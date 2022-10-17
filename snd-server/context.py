from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.sqlite_storage import SqliteStorage
    from services.config import Config


class Context:
    sqlite_storage: "SqliteStorage"
    config: "Config"
