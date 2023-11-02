import json
from typing import Dict

import pika
from lib.utilities import logger
from pika.adapters.blocking_connection import BlockingChannel


def get_channel(uri: str, queue: str) -> BlockingChannel:
    params = pika.URLParameters(uri)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue)
    return channel


def published(channel: BlockingChannel, queue: str, message: Dict[str, str]) -> bool:
    try:
        delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
        properties = pika.BasicProperties(delivery_mode=delivery_mode)

        channel.basic_publish(
            body=json.dumps(message),
            properties=properties,
            routing_key=queue,
            exchange="",
        )
        logger.info("Successfully published message to %s queue", queue)
        return True
    except Exception as error:
        logger.info("Failed to publish message to %s queue", queue)
        logger.error("%s - %s", error.__class__.__name__, error)
        return False
