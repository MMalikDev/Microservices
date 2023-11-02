import sys
import time
from pathlib import Path

if __name__ == "__main__":
    path = str(Path.cwd())
    sys.path.append(path)

from db.setup import database
from lib.stream import initialize_group
from lib.utilities import logger
from models.orders import Order, OrderStatus


def refund_order_stream():
    key = "refund_order"
    group = "payment-group"
    initialize_group(database, key, group)

    while True:
        try:
            if not (results := database.xreadgroup(group, key, {key: ">"}, None)):
                continue

            for result in results:
                logger.debug(result)
                pk = result[1][0][1]["pk"]

                order = Order.get(pk)
                order.status = OrderStatus.REFUNDED
                order.save()

                msg = f"Order {pk} was refunded"
                logger.info(msg)

        except Exception as e:
            logger.error(e)

        time.sleep(1)


def main():
    refund_order_stream()


if __name__ == "__main__":
    main()
