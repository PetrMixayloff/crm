import datetime
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.orm import relationship


class User(Base):
    login = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=True)
    full_name = Column(String(255))
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=True)
    shops = relationship('UserShopRelation')


class Shop(Base):
    name = Column(String(255), unique=True)
    address = Column(String(255), nullable=True)
    staff = relationship('UserShopRelation')
    products = relationship('ProductShopRelation')


class UserShopRelation(Base):
    """ Таблица отношений М-М сотрудников и магазинов"""
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'))
    position = Column(String(255), nullable=True, comment='Должность сотрудника')


class ProductCategory(Base):
    name = Column(String(255), unique=True)
    description = Column(String(255), nullable=True)
    products = relationship('Product')


class Product(Base):
    category_id = Column(UUID(as_uuid=True), ForeignKey('productcategory.id'))
    name = Column(String(255), unique=True)
    description = Column(String(255), nullable=True)
    url = Column(String(255), nullable=True)
    images = relationship('ProductImageRelationship')


class File(Base):
    path = Column(String(255), unique=True)


class ProductImageRelation(Base):
    """ Таблица отношений М-М товаров и изображений"""
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    file_id = Column(UUID(as_uuid=True), ForeignKey('file.id'))


class ProductShopRelation(Base):
    """ Таблица отношений М-М товаров и магазинов"""
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'))
    price = Column(Integer, default=0)
    old_price = Column(Integer, nullable=True)
    quantity = Column(Integer, default=0)


class BlacklistToken(Base):
    """
    Token Model for storing JWT tokens
    """
    token = Column(String, unique=True, index=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False