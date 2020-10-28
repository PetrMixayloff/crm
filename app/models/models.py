import datetime
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey, Integer, Float, UniqueConstraint
from sqlalchemy.orm import relationship


class User(Base):
    phone = Column(String(255), nullable=False, comment='Номер телефона')
    password = Column(String(255), comment='Пароль')
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'))
    full_name = Column(String(255), comment='ФИО')
    last_login = Column(DateTime, comment='Последний вход')
    is_superuser = Column(Boolean, nullable=False, default=False, comment='Права суперпользователя')
    is_staff = Column(Boolean, nullable=False, default=True, comment='Владелец магазина')
    position = Column(String(255), comment='Должность сотрудника')
    description = Column(String(255), comment='Данные')
    avatar = relationship("File", uselist=False)


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
    products = relationship('Product', back_populates="productcategory", cascade="all, delete-orphan")
    show_on_store = Column(Boolean, nullable=False, default=True)


class Product(Base):
    category_id = Column(UUID(as_uuid=True), ForeignKey('productcategory.id'), nullable=False)
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    productcategory = relationship("ProductCategory", back_populates="products")
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    url = Column(String(255))
    images = relationship('File')
    price = Column(Float, default=0)
    old_price = Column(Float, default=0)
    quantity = Column(Integer, default=0)
    show_on_store = Column(Boolean, nullable=False, default=True)


class File(Base):
    __table_args__ = (UniqueConstraint('product_id', 'user_id', name='_product_user_uc'),)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
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