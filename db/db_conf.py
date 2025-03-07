from pydantic_settings import BaseSettings, SettingsConfigDict

class SQLite(BaseSettings):
    DB_FILE: str

    @property
    def DATABASE_URL_sqlite(self):
        return f"sqlite:///{self.DB_FILE}"

sqlite = SQLite()