from lib.utilities import load_variable


class Settings:
    VALIDATE_API: str = load_variable("VALIDATE_API", "http://auth:8080/validate")
    LOGIN_API: str = load_variable("LOGIN_API", "http://auth:8080/login")
    MONGO_URI: str = load_variable("MONGO_URI", "mongo:27017")
    QUEUE_URI: str = load_variable("QUEUE_URI", "rabbitmq")
    VIDEO_QUEUE: str = load_variable("VIDEO_QUEUE")
    API_HOST: str = load_variable("API_HOST", "0.0.0.0")
    API_PORT: int = int(load_variable("API_PORT", "8080"))


settings = Settings()
