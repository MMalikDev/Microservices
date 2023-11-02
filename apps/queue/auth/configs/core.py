from lib.utilities import load_variable


class Settings:
    DATABASE_URI: str = load_variable("DATABASE_URI", "sqlite+pysqlite:///sqlite.db")
    SUPERUSER_EMAIL: str = load_variable("SUPERUSER_EMAIL", "admin@email.com")
    SUPERUSER_PASSWORD: str = load_variable("SUPERUSER_PASSWORD", "pass")
    JWT_SECRET: str = load_variable("JWT_SECRET", "secret")
    API_HOST: str = load_variable("API_HOST", "0.0.0.0")
    API_PORT: int = int(load_variable("API_PORT", "8080"))


settings = Settings()
