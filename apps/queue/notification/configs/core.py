from lib.utilities import load_variable


class Settings:
    QUEUE_URI: str = load_variable("QUEUE_URI", "rabbitmq")
    AUDIO_QUEUE: str = load_variable("AUDIO_QUEUE", "audio")
    EMAIL_ADDRESS: str = load_variable("EMAIL_ADDRESS")
    EMAIL_PASSWORD: str = load_variable("EMAIL_PASSWORD")


settings = Settings()
