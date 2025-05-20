from app.config.config import DEFAULT_CATEGORY
from typing import Union, Optional
from app.db.models import (
    Product
)
from app.db.base import (
    Session
)


def get_all_products_filtered(min_price: float = 0, max_price: float = 1000000, category_id: int = None):
    with Session() as session:
        products = session.query(Product).filter(
            Product.price >= min_price,
            Product.price <= max_price,
            )

        if category_id:
            products = products.filter(Product.category_id == category_id)

        return products.all()

def get_product_by_id(product_id: int) -> Product.to_dict:
    with Session() as session:
        product = session.query(Product).filter_by(id=product_id).one_or_none()

        if not product:
            raise ValueError('Product not found')

        return product.to_dict()

def add_product(
        title: str,
        description: str,
        price: float,
        images: str,
        category_id: int,
        user_id: int
) -> Union[Product, Optional[ValueError]]:
    with Session() as session:

        if price < 0:
            raise ValueError("Invalid price")
        elif category_id > len(DEFAULT_CATEGORY):
            raise ValueError("Invalid category_id")

        product = Product(title=title, description=description, price=price,
                          images=images, category_id=category_id, user_id=user_id)

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

def remove_product(
        product_id: int,
        user_id: int
) -> Product.to_dict:
    with Session() as session:
        product = session.query(Product).filter_by(id=product_id).one_or_none()

        if not product:
            raise ValueError("Unknown product_id")
        elif product.user_id != user_id:
            raise ValueError("You do not have permission to perform this action")

        product_info = product.to_dict()

        session.delete(product)
        session.commit()

        return product_info
