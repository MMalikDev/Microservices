from config.core import settings
from redis import StrictRedis

database = StrictRedis.from_url(settings.DATABASE_URI, decode_responses=True)
