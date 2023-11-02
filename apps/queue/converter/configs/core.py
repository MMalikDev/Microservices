from lib.utilities import load_variable


class Settings:
    MONGO_URI: str = load_variable("MONGO_URI", "mongo:27017")
    QUEUE_URI: str = load_variable("QUEUE_URI", "rabbitmq")
    VIDEO_QUEUE: str = load_variable("VIDEO_QUEUE", "video")
    AUDIO_QUEUE: str = load_variable("AUDIO_QUEUE", "audio")


settings = Settings()
