import json
import tempfile
from typing import Dict

import moviepy
from bson.objectid import ObjectId
from configs.core import settings
from gridfs import GridFS
from lib import database, queue
from lib.utilities import debug, logger
from pika import spec
from pika.adapters.blocking_connection import BlockingChannel


def convert_to_audio(
    channel: BlockingChannel, message: str, db_video: GridFS, db_audio: GridFS
) -> None:
    message: Dict[str, str] = json.loads(message)
    video_id = message.get("video_id")

    # Get video from DB and extract Audio
    contents = db_video.get(ObjectId(video_id))
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(contents.read())
        audio = moviepy.VideoFileClip(temp.name).audio
        temp.flush()

    # Get audio file bytes data
    with tempfile.NamedTemporaryFile(suffix=".mp3") as temp:
        audio.write_audiofile(temp.name)
        data = temp.read()
        temp.flush()

    # Save data to MongoDB
    id = db_audio.put(data)
    message["audio_id"] = str(id)
    if not queue.published(channel, settings.AUDIO_QUEUE, message):
        db_audio.delete(id)
        logger.info("Deleted Incomplete Audio with ID: %s", id)


@debug
def main():
    db_video = database.get_db("video")
    db_audio = database.get_db("audio")

    def callback(
        ch: BlockingChannel,
        method: spec.Basic.Deliver,
        _properties: spec.BasicProperties,
        body: bytes,
    ) -> None:
        convert_to_audio(ch, body, db_video, db_audio)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel = queue.get_channel(settings.QUEUE_URI, settings.VIDEO_QUEUE)
    channel.basic_consume(queue=settings.VIDEO_QUEUE, on_message_callback=callback)
    logger.info("Waiting for messages.")
    channel.start_consuming()


if __name__ == "__main__":
    main()
