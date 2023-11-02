import json
import smtplib
from email.message import EmailMessage

from configs.core import settings
from lib import queue
from lib.utilities import debug, logger
from pika import spec
from pika.adapters.blocking_connection import BlockingChannel


def send_email(message: EmailMessage, receiver: str) -> None:
    if not settings.EMAIL_ADDRESS or not settings.EMAIL_PASSWORD:
        msg = "No Sender Credentials Provided - Skipping email notification"
        logger.info(msg)
        return

    message["From"] = settings.EMAIL_ADDRESS
    message["To"] = receiver
    logger.debug("Message: %s", str(message))

    with smtplib.SMTP("smtp.gmail.com", 587) as session:
        session.ehlo()  # Identify ourselves to the smtp gmail client
        session.starttls()  # Secure our email with tls encryption
        session.ehlo()  # Re-identify ourselves as an encrypted connection
        session.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        session.send_message(message, settings.EMAIL_ADDRESS, receiver)

    logger.info("Mail Sent")


def send_notification(message: str) -> None:
    message = json.loads(message)
    receiver = message["username"]
    id = message["audio_id"]

    msg = EmailMessage()
    msg["Subject"] = "Audio Download"
    msg.set_content(f"Audio File ID: {id} is now ready!")
    send_email(msg, receiver)

    logger.info("Notified %s about Audio File ID: %s", receiver, id)


def callback(
    ch: BlockingChannel,
    method: spec.Basic.Deliver,
    _properties: spec.BasicProperties,
    body: bytes,
) -> None:
    send_notification(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


@debug
def main():
    channel = queue.get_channel(settings.QUEUE_URI, settings.AUDIO_QUEUE)
    channel.basic_consume(queue=settings.AUDIO_QUEUE, on_message_callback=callback)
    logger.info("Waiting for messages.")
    channel.start_consuming()


if __name__ == "__main__":
    main()
