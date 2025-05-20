from app.config.config import DEFAULT_CATEGORY
from app.db.base import (
    Session
)
from app.db.models.category import (
    Category
)


def create_categories() -> None:
    with Session() as session:
        objects = []
        for title in DEFAULT_CATEGORY:
            objects.append(
                Category(title=title)
            )
        session.bulk_save_objects(objects)
        session.commit()