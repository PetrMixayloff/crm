"""create_tables

Revision ID: 91a68f86769b
Revises: 
Create Date: 2021-03-25 14:48:34.182503

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '91a68f86769b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('street', sa.String(length=255), nullable=True, comment='Улица/мкрн'),
    sa.Column('house', sa.String(length=255), nullable=True, comment='Дом'),
    sa.Column('entrance', sa.String(length=255), nullable=True, comment='Подъезд'),
    sa.Column('floor', sa.String(length=255), nullable=True, comment='Этаж'),
    sa.Column('flat', sa.String(length=255), nullable=True, comment='Кв/офис'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blacklisttoken',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blacklisttoken_token'), 'blacklisttoken', ['token'], unique=True)
    op.create_table('shop',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cancellation',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('number', sa.String(length=255), nullable=True, comment='Номер'),
    sa.Column('date', sa.DateTime(), nullable=True, comment='Дата'),
    sa.Column('supplier', sa.String(length=255), nullable=True, comment='Поставщик'),
    sa.Column('remark', sa.String(length=255), nullable=True, comment='Примечание'),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=False, comment='Номер телефона'),
    sa.Column('name', sa.String(length=255), nullable=True, comment='Имя'),
    sa.Column('sex', sa.String(length=255), nullable=True, comment='Пол'),
    sa.Column('age', sa.Integer(), nullable=True, comment='Возраст'),
    sa.Column('address', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('discount_card', sa.String(length=255), nullable=True, comment='Дисконтная карта'),
    sa.Column('comment', sa.String(length=255), nullable=True, comment='Примечание'),
    sa.ForeignKeyConstraint(['address'], ['address.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoice',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('number', sa.String(length=255), nullable=True, comment='Номер'),
    sa.Column('date', sa.DateTime(), nullable=True, comment='Дата'),
    sa.Column('supplier', sa.String(length=255), nullable=True, comment='Поставщик'),
    sa.Column('remark', sa.String(length=255), nullable=True, comment='Примечание'),
    sa.Column('payment_method', sa.String(length=255), nullable=True, comment='Способ оплаты'),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productcategory',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('show_on_store', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rawcategory',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True, comment='Название категории'),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True, comment='Id родительской категории'),
    sa.Column('description', sa.String(length=255), nullable=True, comment='Описание'),
    sa.ForeignKeyConstraint(['parent_id'], ['rawcategory.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('phone', sa.String(length=255), nullable=False, comment='Номер телефона'),
    sa.Column('password', sa.String(length=255), nullable=True, comment='Пароль'),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('full_name', sa.String(length=255), nullable=True, comment='ФИО'),
    sa.Column('last_login', sa.DateTime(), nullable=True, comment='Последний вход'),
    sa.Column('is_superuser', sa.Boolean(), nullable=False, comment='Права суперпользователя'),
    sa.Column('is_staff', sa.Boolean(), nullable=False, comment='Владелец магазина'),
    sa.Column('position', sa.String(length=255), nullable=True, comment='Должность сотрудника'),
    sa.Column('description', sa.String(length=255), nullable=True, comment='Данные'),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True, comment='Ответственный сотрудник'),
    sa.Column('number', sa.String(length=255), nullable=True, comment='Номер'),
    sa.Column('date', sa.DateTime(), nullable=True, comment='Дата'),
    sa.Column('remark', sa.String(length=255), nullable=True, comment='Примечание'),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('order_number', sa.Integer(), autoincrement=True, nullable=False, comment='№ заказа'),
    sa.Column('created_by_id', postgresql.UUID(as_uuid=True), nullable=True, comment='Принял'),
    sa.Column('make_by_id', postgresql.UUID(as_uuid=True), nullable=True, comment='Выполнил'),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('delivery', sa.Boolean(), nullable=False, comment='Доставка/самовывоз'),
    sa.Column('delivery_cost', sa.Float(), nullable=True, comment='Стоимость доставки'),
    sa.Column('decoration_cost', sa.Float(), nullable=True, comment='Стоимость монтажа'),
    sa.Column('courier_id', postgresql.UUID(as_uuid=True), nullable=True, comment='Курьер'),
    sa.Column('total_cost', sa.Float(), nullable=False, comment='Сумма заказа'),
    sa.Column('reason', sa.String(length=255), nullable=True, comment='Повод для заказа'),
    sa.Column('sales_channel', sa.String(length=255), nullable=True, comment='Канал продаж'),
    sa.Column('prepay', sa.Float(), nullable=True, comment='Предоплата'),
    sa.Column('prepay_type', sa.String(length=255), nullable=True, comment='Тип внесения предоплаты'),
    sa.Column('amount', sa.Float(), nullable=False, comment='К оплате с учетом предоплаты'),
    sa.Column('amount_type', sa.String(length=255), nullable=True, comment='Тип внесения оплаты'),
    sa.Column('discount', sa.Float(), nullable=True, comment='Скидка'),
    sa.Column('discount_card', sa.String(length=255), nullable=True, comment='Дисконтная карта'),
    sa.Column('promo', sa.String(length=255), nullable=True, comment='Промокод'),
    sa.Column('rating', sa.Integer(), nullable=True, comment='Оценка от клиента'),
    sa.Column('status', sa.String(length=255), nullable=True, comment='Статус'),
    sa.Column('date_created', sa.DateTime(), nullable=True, comment='Дата поступления'),
    sa.Column('date_of_order', sa.DateTime(), nullable=False, comment='Дата заказа'),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['courier_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['make_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_number')
    )
    op.create_table('product',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False, comment='Название'),
    sa.Column('description', sa.String(length=255), nullable=True, comment='Описание'),
    sa.Column('image', sa.String(length=255), nullable=True, comment='Изображение'),
    sa.Column('price', sa.Float(), nullable=True, comment='Цена'),
    sa.Column('old_price', sa.Float(), nullable=True, comment='Старая цена'),
    sa.Column('show_on_store', sa.Boolean(), nullable=False, comment='Отображать на витрине'),
    sa.ForeignKeyConstraint(['category_id'], ['productcategory.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('raw',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Категория'),
    sa.Column('reserved', sa.Float(), nullable=True, comment='Зарезервировано'),
    sa.Column('name', sa.String(length=255), nullable=False, comment='Название'),
    sa.Column('description', sa.String(length=255), nullable=True, comment='Описание'),
    sa.Column('per_pack', sa.Integer(), nullable=True, comment='В упаковке'),
    sa.Column('green_signal', sa.Integer(), nullable=True, comment='Зеленая метка'),
    sa.Column('yellow_signal', sa.Integer(), nullable=True, comment='Желтая метка'),
    sa.Column('red_signal', sa.Integer(), nullable=True, comment='Красная метка'),
    sa.Column('unit', sa.String(length=255), nullable=True, comment='Ед. измерения'),
    sa.Column('image', sa.String(length=255), nullable=True, comment='Изображение'),
    sa.ForeignKeyConstraint(['category_id'], ['rawcategory.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventoryrecord',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('inventory_id', postgresql.UUID(as_uuid=True), nullable=False, comment='ИНВ Опись'),
    sa.Column('raw_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Название'),
    sa.Column('quantity', sa.Float(), nullable=True, comment='Количество'),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], ),
    sa.ForeignKeyConstraint(['raw_id'], ['raw.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoicerecord',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('invoice_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Накладная'),
    sa.Column('raw_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Id сырья'),
    sa.Column('price', sa.Float(), nullable=True, comment='Цена за ед.'),
    sa.Column('quantity', sa.Float(), nullable=True, comment='Количество'),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
    sa.ForeignKeyConstraint(['raw_id'], ['raw.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ordersproductsrelation',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rawremainsdetail',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('raw_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Название'),
    sa.Column('invoice_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Накладная'),
    sa.Column('price', sa.Float(), nullable=True, comment='Цена за ед.'),
    sa.Column('quantity', sa.Float(), nullable=True, comment='Количество'),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
    sa.ForeignKeyConstraint(['raw_id'], ['raw.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rawusagestandards',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('raw_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Сырье'),
    sa.Column('name', sa.String(length=255), nullable=False, comment='Название стандарта'),
    sa.Column('quantity', sa.Float(), nullable=True, comment='Количество сырья на ед. стандарта'),
    sa.ForeignKeyConstraint(['raw_id'], ['raw.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cancellationrecord',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('shop_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('cancellation_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Списание'),
    sa.Column('rawremainsdetail_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Id сырья в остатках'),
    sa.Column('quantity', sa.Float(), nullable=True, comment='Количество'),
    sa.ForeignKeyConstraint(['cancellation_id'], ['cancellation.id'], ),
    sa.ForeignKeyConstraint(['rawremainsdetail_id'], ['rawremainsdetail.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ordersproductsrawrelation',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('order_product_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('raw_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('standard_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_product_id'], ['ordersproductsrelation.id'], ),
    sa.ForeignKeyConstraint(['raw_id'], ['raw.id'], ),
    sa.ForeignKeyConstraint(['standard_id'], ['rawusagestandards.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('productrawrelation',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('raw_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('standard_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['raw_id'], ['raw.id'], ),
    sa.ForeignKeyConstraint(['standard_id'], ['rawusagestandards.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('productrawrelation')
    op.drop_table('ordersproductsrawrelation')
    op.drop_table('cancellationrecord')
    op.drop_table('rawusagestandards')
    op.drop_table('rawremainsdetail')
    op.drop_table('ordersproductsrelation')
    op.drop_table('invoicerecord')
    op.drop_table('inventoryrecord')
    op.drop_table('raw')
    op.drop_table('product')
    op.drop_table('orders')
    op.drop_table('inventory')
    op.drop_table('user')
    op.drop_table('rawcategory')
    op.drop_table('productcategory')
    op.drop_table('invoice')
    op.drop_table('client')
    op.drop_table('cancellation')
    op.drop_table('shop')
    op.drop_index(op.f('ix_blacklisttoken_token'), table_name='blacklisttoken')
    op.drop_table('blacklisttoken')
    op.drop_table('address')
    # ### end Alembic commands ###