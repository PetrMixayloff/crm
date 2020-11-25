import datetime
from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey, Integer, Float, ARRAY
from sqlalchemy.orm import relationship


class Orders(Base):
    created_by_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    created_by = relationship("User", foreign_keys='Orders.created_by_id')
    make_by_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    make_by = relationship("User", foreign_keys='Orders.make_by_id')
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'))
    client_id = Column(UUID(as_uuid=True), ForeignKey('client.id'))
    products = relationship('OrdersProductsRelation')
    delivery = Column(Boolean, nullable=False, default=False, comment='Доставка/самовывоз')
    courier_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    courier = relationship("User", foreign_keys='Orders.courier_id')
    total_cost = Column(Float, nullable=False, comment='Сумма заказа')
    prepay = Column(Float, default=0, comment='Предоплата')
    prepay_type = Column(String(255), comment='Тип внесения предоплаты')
    amount = Column(Float, nullable=False, comment='К оплате с учетом предоплаты')
    amount_type = Column(String(255), comment='Тип внесения оплаты')
    discount = Column(Float, default=0, comment='Скидка')
    rating = Column(Integer, comment='Оценка от клиента')
    status = Column(String(255), comment='Статус')
    date_created = Column(DateTime, default=datetime.datetime.now)
    date_of_order = Column(DateTime, nullable=False)


class OrdersProductsRelation(Base):
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id', ondelete="CASCADE"))
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    quantity = Column(Integer, nullable=False)


class Client(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'))
    phone = Column(String(255), nullable=False, comment='Номер телефона')
    name = Column(String(255), nullable=False, comment='Имя')
    address = Column(String(255), comment='Адрес')
    orders = relationship("Orders")
    discount = Column(String(255), comment='Дисконтная карта')
    comment = Column(String(255), comment='Примечание')


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
    avatar = Column(String(255))


class Shop(Base):
    name = Column(String(255), nullable=False)
    address = Column(String(255))
    users = relationship("User")
    products_categories = relationship('ProductCategory')
    products = relationship('Product')
    raw_categories = relationship('RawCategory')
    raw = relationship('Raw')


class ProductCategory(Base):
    name = Column(String(255))
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    description = Column(String(255))
    products = relationship('Product', back_populates="productcategory", cascade="all, delete-orphan")
    show_on_store = Column(Boolean, nullable=False, default=True)


class Product(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('productcategory.id'), nullable=False)
    productcategory = relationship("ProductCategory", back_populates="products")
    raw = relationship('ProductRawRelation', cascade="all, delete-orphan")
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    url = Column(String(255))
    images = Column(ARRAY(String))
    price = Column(Float, default=0)
    old_price = Column(Float, default=0)
    show_on_store = Column(Boolean, nullable=False, default=True)


class ProductRawRelation(Base):
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id'))
    quantity = Column(Integer, default=0)
    raw = relationship("Raw", back_populates="products")
    product = relationship("Product", back_populates="raw")


class RawCategory(Base):
    name = Column(String(255))
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    raws = relationship('Raw', back_populates="raw_category", cascade="all, delete-orphan")
    description = Column(String(255))


class Raw(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('rawcategory.id'), nullable=False, comment='Категория')
    raw_category = relationship("RawCategory", back_populates="raws")
    products = relationship("ProductRawRelation", cascade="all, delete-orphan")
    name = Column(String(255), nullable=False, comment='Название')
    description = Column(String(255), comment='Описание')
    price = Column(Float, default=0, comment='Суммарная стоимость остатка')
    quantity = Column(Integer, default=0, comment='Общий остаток')
    per_pack = Column(Integer, default=0, comment='В упаковке')
    green_signal = Column(Integer, default=0, comment='Зеленая метка')
    yellow_signal = Column(Integer, default=0, comment='Желтая метка')
    red_signal = Column(Integer, default=0, comment='Красная метка')
    unit = Column(String(255), comment='Ед. измерения')
    image = Column(String(255), comment='Изображение')


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