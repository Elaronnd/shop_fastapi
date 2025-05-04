from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from typing import (
    List
)

from app.db.base import (
    Base
)

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)

    products: Mapped[List['Product']] = relationship(back_populates='category')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title
        }

    def __repr__(self):
        return f'Category(id={self.id}, title={self.title})'