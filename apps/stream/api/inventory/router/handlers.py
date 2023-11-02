from models.products import Product


# ---------------------------------------------------------------------- #
# Query Handling
# ---------------------------------------------------------------------- #
def pagination(data: list, page: int = 1, limit: int = 100) -> list:
    startIndex = (page - 1) * limit
    endIndex = page * limit

    data = data[startIndex:endIndex]
    return data


def format(pk: str) -> dict:
    product = Product.get(pk)

    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
    }


# ---------------------------------------------------------------------- #
# Error Handling
# ---------------------------------------------------------------------- #
def not_found_msg(id) -> str:
    return f"Product with ID {id} not found"
