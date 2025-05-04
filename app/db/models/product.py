from sqlalchemy import (
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.base import (
    Base,
)

import base64

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    image: Mapped[bytes] = mapped_column(nullable=False)

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
            'image': base64.b64encode(self.image).decode('utf-8'),
            'category_id': self.category_id,
            'user_id': self.user_id,
        }

    def __repr__(self):
        return f'Product(id={self.id}, title={self.title}, description={self.description}, price={self.price}),category_id={self.category_id}, user_id={self.user_id})'