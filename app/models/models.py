import datetime

from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey, Integer, Float, ARRAY, Sequence
from sqlalchemy.orm import relationship


class Orders(Base):
    orders_number_seq = Sequence('number_seq')
    order_number = Column(Integer, nullable=False, server_default=orders_number_seq.next_value(), comment='№ заказа')
    created_by_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), comment='Принял')
    make_by_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), comment='Выполнил')
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'))
    client_id = Column(UUID(as_uuid=True), ForeignKey('client.id'))
    client = relationship("Client", back_populates="orders")
    products = relationship('OrdersProductsRelation', cascade="all, delete-orphan")
    delivery = Column(Boolean, nullable=False, default=False, comment='Доставка/самовывоз')
    delivery_cost = Column(Float, comment='Стоимость доставки')
    decoration_cost = Column(Float, comment='Стоимость монтажа')
    courier_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), comment='Курьер')
    total_cost = Column(Float, nullable=False, comment='Сумма заказа')
    reason = Column(String(255), comment='Повод для заказа')
    sales_channel = Column(String(255), comment='Канал продаж')
    prepay = Column(Float, default=0, comment='Предоплата')
    prepay_type = Column(String(255), comment='Тип внесения предоплаты')
    amount = Column(Float, nullable=False, comment='К оплате с учетом предоплаты')
    amount_type = Column(String(255), comment='Тип внесения оплаты')
    discount = Column(Float, default=0, comment='Скидка')
    discount_card = Column(String(255), comment='Дисконтная карта')
    promo = Column(String(255), comment='Промокод')
    rating = Column(Integer, comment='Оценка от клиента')
    status = Column(String(255), comment='Статус')
    date_created = Column(DateTime, default=datetime.datetime.now, comment='Дата поступления')
    date_of_order = Column(DateTime, nullable=False, comment='Дата заказа')
    remark = Column(String(255), comment='Примечание к заказу')


class OrdersProductsRelation(Base):
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id', ondelete="CASCADE"))
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    price = Column(Float, nullable=False, comment='Цена')
    name = Column(String(255), nullable=True, comment='Название')
    image = Column(String(255), comment='Изображение')
    quantity = Column(Integer, nullable=False)
    raw = relationship('OrdersProductsRawRelation', cascade="all, delete-orphan")


class OrdersProductsRawRelation(Base):
    order_product_id = Column(UUID(as_uuid=True), ForeignKey('orders_products_relation.id'))
    raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id'))
    standard_id = Column(UUID(as_uuid=True), ForeignKey('raw_usage_standards.id'))
    quantity = Column(Integer, default=0)


class Client(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'))
    phone = Column(String(255), nullable=False, comment='Номер телефона')
    name = Column(String(255), comment='Имя')
    sex = Column(String(255), comment='Пол')
    age = Column(Integer, comment='Возраст')
    address = relationship('Address', uselist=False, cascade="all, delete-orphan")
    orders = relationship("Orders", back_populates="client")
    discount_card = Column(String(255), comment='Дисконтная карта')
    comment = Column(String(255), comment='Примечание')


class Address(Base):
    street = Column(String(255), comment='Улица/мкрн')
    house = Column(String(255), comment='Дом')
    entrance = Column(String(255), comment='Подъезд')
    floor = Column(String(255), comment='Этаж')
    flat = Column(String(255), comment='Кв/офис')
    client_id = Column(UUID(as_uuid=True), ForeignKey('client.id'))


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
    permissions = relationship('Permissions', lazy='joined', uselist=False, cascade="all, delete-orphan")
    avatar = Column(String(255))


class Permissions(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    orders = Column(String(255), comment='Права на работу с заказами')
    products = Column(String(255), comment='Права на работу с продуктами')
    raw = Column(String(255), comment='Права на работу с сырьем')
    clients = Column(String(255), comment='Права на работу с клиентами')
    staff = Column(String(255), comment='Права на работу с персоналом')
    warehouse = Column(String(255), comment='Права на работу со складом')


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
    products = relationship('Product', back_populates="product_category", cascade="all, delete-orphan")
    show_on_store = Column(Boolean, nullable=False, default=True)


class Product(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('product_category.id'), nullable=False)
    product_category = relationship("ProductCategory", back_populates="products")
    raw = relationship('ProductRawRelation', cascade="all, delete-orphan")
    base = Column(Boolean, nullable=False, default=True, comment='Базовый товар')
    name = Column(String(255), nullable=False, comment='Название')
    description = Column(String(255), comment='Описание')
    image = Column(String(255), comment='Изображение')
    price = Column(Float, default=0, comment='Цена')
    old_price = Column(Float, comment='Старая цена')
    show_on_store = Column(Boolean, nullable=False, default=True, comment='Отображать на витрине')
    product_set_id = Column(UUID(as_uuid=True), index=True, unique=True, nullable=True)
    products = relationship('ProductSetRelation',
                            primaryjoin="Product.product_set_id==ProductSetRelation.product_set_id",
                            cascade="all, delete-orphan")


class ProductSetRelation(Base):
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    product_set_id = Column(UUID(as_uuid=True), ForeignKey('product.product_set_id'))
    quantity = Column(Float, default=0)


class ProductRawRelation(Base):
    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'))
    raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id'))
    standard_id = Column(UUID(as_uuid=True), ForeignKey('raw_usage_standards.id'))
    quantity = Column(Float, default=0)
    raw = relationship("Raw", back_populates="products")
    product = relationship("Product", back_populates="raw")


class RawCategory(Base):
    name = Column(String(255), comment='Название категории')
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('raw_category.id'), comment='Id родительской категории')
    raw = relationship('Raw', back_populates="raw_category", cascade="all, delete-orphan")
    description = Column(String(255), comment='Описание')
    subcategories = relationship("RawCategory", primaryjoin="RawCategory.id==RawCategory.parent_id")


class Raw(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('raw_category.id'),
                         nullable=False, comment='Категория')
    piece_raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id', ondelete="SET NULL"), comment='Id разборного сырья')
    name = Column(String(255), nullable=False, comment='Название')
    article_number = Column(String(255), comment='Артикул')
    manufacturer = Column(String(255), comment='Производитель')
    unit = Column(String(255), comment='Ед. измерения')
    piece_unit = Column(String(255), comment='Ед. измерения разборного сырья')
    per_pack = Column(Float, default=0, comment='В упаковке')
    helium_consumption = Column(Float, default=0, comment='Расход гелия')
    yellow_label = Column(Float, default=0, comment='Желтая метка')
    red_label = Column(Float, default=0, comment='Красная метка')
    description = Column(String(255), comment='Описание')
    image = Column(String(255), comment='Изображение')
    raw_category = relationship("RawCategory", back_populates="raw")
    quantity = Column(Float, default=0, comment='Текущий остаток на складе')
    reserved = Column(Float, default=0, comment='Зарезервировано')
    available_quantity = Column(Float, default=0, comment='Остаток с учетом зарезервированного количества')
    products = relationship("ProductRawRelation", cascade="all, delete-orphan")
    remains = relationship('RawRemainsDetail')
    standards = relationship('RawUsageStandards')


class RawUsageStandards(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id'), nullable=False, comment='Сырье')
    name = Column(String(255), nullable=False, comment='Название стандарта')
    quantity = Column(Float, default=0, comment='Количество сырья на ед. стандарта')


class RawRemainsDetail(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id'), nullable=False, comment='Название')
    invoice_id = Column(UUID(as_uuid=True), ForeignKey('invoice.id'), comment='Id накладной')
    inventory_id = Column(UUID(as_uuid=True), ForeignKey('inventory.id'), comment='Id документа инвентаризации')
    opening_id = Column(UUID(as_uuid=True), ForeignKey('opening.id'), comment='Id документа разборки')
    # invoice = Column(Boolean, nullable=False, comment='True: приходная накладная, False: инвентаризация')
    number = Column(String(255), comment='Номер')
    date = Column(DateTime, comment='Дата')
    quantity = Column(Float, default=0, comment='Оставшееся количество')
    price = Column(Float, default=0, comment='Цена за ед.')


class RawRemainsLog(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id'), nullable=False, comment='Название')
    arrival = Column(Boolean, nullable=False, comment='True: приход, False: расход')
    action = Column(String(255), nullable=False, comment='Событие: приход, списание, инвентаризация, продажа, разборка')
    number = Column(String(255), nullable=False, comment='Номер')
    date = Column(DateTime, nullable=False, comment='Дата')
    quantity = Column(Float, default=0, comment='Количество')
    total = Column(Float, default=0, comment='Общее количество после события')


class Inventory(Base):
    inventory_number_seq = Sequence('number_seq')
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), comment='Ответственный сотрудник')
    number = Column(Integer, nullable=False, server_default=inventory_number_seq.next_value(), comment='Номер')
    date = Column(DateTime, comment='Дата')
    remark = Column(String(255), comment='Примечание')
    records = relationship("InventoryRecord", back_populates='inventory', cascade="all, delete-orphan")


class InventoryRecord(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    inventory_id = Column(UUID(as_uuid=True), ForeignKey('inventory.id'), nullable=False, comment='ИНВ Опись')
    raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id'), nullable=False, comment='Название')
    quantity = Column(Float, default=0, comment='Остаток по факту инвентаризации')
    old_quantity = Column(Float, default=0, comment='Остаток по программе')
    inventory = relationship('Inventory', back_populates='records')


class Invoice(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    number = Column(String(255), comment='Номер')
    date = Column(DateTime, comment='Дата')
    supplier = Column(String(255), comment='Поставщик')
    remark = Column(String(255), comment='Примечание')
    payment_method = Column(String(255), comment='Способ оплаты')
    records = relationship('InvoiceRecord', back_populates="invoice", cascade="all, delete-orphan")


class InvoiceRecord(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey('invoice.id'), nullable=False, comment='Накладная')
    invoice = relationship("Invoice", back_populates="records")
    raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id'), nullable=False, comment='Id сырья')
    price = Column(Float, default=0, comment='Цена за ед.')
    quantity = Column(Float, default=0, comment='Количество')


class Cancellation(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    cancel_number_seq = Sequence('number_seq')
    number = Column(Integer, nullable=False, server_default=cancel_number_seq.next_value(), comment='Номер')
    date = Column(DateTime, comment='Дата')
    reason = Column(String(255), comment='Причина')
    remark = Column(String(255), comment='Примечание')
    records = relationship('CancellationRecord', back_populates="cancellation", cascade="all, delete-orphan")


class CancellationRecord(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    cancellation_id = Column(UUID(as_uuid=True), ForeignKey('cancellation.id'), nullable=False, comment='Списание')
    raw_remains_details_id = Column(UUID(as_uuid=True), ForeignKey('raw_remains_detail.id'), nullable=False)
    cancellation = relationship("Cancellation", back_populates="records")
    raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id'), nullable=False, comment='Id сырья в остатках')
    quantity = Column(Float, default=0, comment='Количество')
    price = Column(Float, default=0, comment='Цена за ед.')


class Opening(Base):
    shop_id = Column(UUID(as_uuid=True), ForeignKey('shop.id'), nullable=False)
    opening_number_seq = Sequence('number_seq')
    number = Column(Integer, nullable=False, server_default=opening_number_seq.next_value(), comment='Номер')
    date = Column(DateTime, comment='Дата', default=datetime.datetime.utcnow())
    remark = Column(String(255), comment='Примечание')
    raw_remains_details_id = Column(UUID(as_uuid=True), ForeignKey('raw_remains_detail.id'), nullable=False)
    raw_id = Column(UUID(as_uuid=True), ForeignKey('raw.id'), nullable=False, comment='Id сырья в остатках')


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
