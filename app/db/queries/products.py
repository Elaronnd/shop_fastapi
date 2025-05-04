from app.db.models import (
    Product
)

from app.db.base import (
    Session
)

def get_all_products_filtered(min_price: float = 0, max_price: float = 100000, category_id: int = None):
    with Session() as session:
        products = session.query(Product).filter(
            Product.price >= min_price,
            Product.price <= max_price,
            )

        if category_id:
            producst = products.filter(Product.category_id == category_id)

        return products.all()