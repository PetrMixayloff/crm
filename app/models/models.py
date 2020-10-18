import datetime
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship


class User(Base):
    login = Column(String(255), nullable=False)
    password = Column(String(255))
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'))
    full_name = Column(String(255))
    last_login = Column(DateTime)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=True)
    position = Column(String(255), comment='Должность сотрудника')


class Shop(Base):
    name = Column(String(255), nullable=False)
    address = Column(String(255))
    users = relationship("User")
    products_categories = relationship('ProductCategory')
    products = relationship('Product')


class ProductCategory(Base):
    name = Column(String(255))
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    description = Column(String(255))
    products = relationship('Product')
    show_on_store = Column(Boolean, nullable=False, default=True)


class Product(Base):
    category_id = Column(UUID(as_uuid=True), ForeignKey('productcategory.id'), nullable=False)
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    url = Column(String(255))
    images = relationship('File')
    price = Column(Float, default=0)
    old_price = Column(Float, default=0)
    quantity = Column(Integer, default=0)
    show_on_store = Column(Boolean, nullable=False, default=True)


class File(Base):
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'), nullable=False)
    path = Column(String(255), unique=True, nullable=False)


class BlacklistToken(Base):
    """
    Token Model for storing JWT tokens
    """
    token = Column(String, unique=True, index=True, nullable=False)
    blacklisted_on = Column(DateTime, default=datetime.datetime.utcnow())

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False