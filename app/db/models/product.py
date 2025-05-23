import json

from app.db.base import Base
from sqlalchemy import (
    ForeignKey,
    TEXT
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    images: Mapped[list[str]] = mapped_column(TEXT, nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    category: Mapped['Category'] = relationship(back_populates='products')

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='products')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'images': json.loads(self.images),
            'category_id': self.category_id,
            'user_id': self.user_id,
        }

    def __repr__(self):
        return f'Product(id={self.id}, title={self.title}, description={self.description}, price={self.price}), images={json.loads(self.images)}, category_id={self.category_id}, user_id={self.user_id})'