from app.db.base import create_db
from app.db.models.product import Product
from app.db.models.user import User
from app.db.models.category import Category
from os.path import exists
from app.db.queries.category import create_categories


async def first_start():
    if not exists("shop.db"):
        create_db()
        create_categories()
