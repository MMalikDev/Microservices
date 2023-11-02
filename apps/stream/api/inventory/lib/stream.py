from lib.utilities import logger
from redis import StrictRedis


def initialize_group(database: StrictRedis, key: str, group: str) -> None:
    try:
        database.xgroup_create(key, group, mkstream=True)
    except Exception as e:
        logger.error(e)
