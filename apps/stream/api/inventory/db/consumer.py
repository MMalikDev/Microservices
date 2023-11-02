import sys
import time
from pathlib import Path

if __name__ == "__main__":
    path = str(Path.cwd())
    sys.path.append(path)

from db.setup import database
from lib.stream import initialize_group
from lib.utilities import logger
from models.products import Product


def order_completion_stream():
    key = "order_completed"
    group = "inventory-group"
    initialize_group(database, key, group)

    while True:
        try:
            if not (results := database.xreadgroup(group, key, {key: ">"}, None)):
                continue

            for result in results:
                logger.debug(result)
                data = result[1][0][1]
                pk = data["product_id"]
                ordered_quantity = int(data["quantity"])

                try:
                    product = Product.get(pk)
                    product.quantity -= ordered_quantity

                    if product.quantity < 0:
                        database.xadd("refund_order", data, "*")
                        continue

                    product.save()

                    msg = f"Product quantity for{pk} reduced by {ordered_quantity}"
                    msg += f"\nNew quantity: {product.quantity}"
                    logger.info(msg)

                except:
                    database.xadd("refund_order", data, "*")

        except Exception as e:
            logger.error(e)

        time.sleep(1)


def main():
    order_completion_stream()


if __name__ == "__main__":
    main()
