from .crud_user import user
from .crud_shop import shop
from .crud_product import product
from .crud_product_category import product_category
from .crud_raw import raw
from .crud_raw_category import raw_category
from .crud_invoice import invoice
from .crud_inventory import inventory
from .crud_order import order
from .crud_client import client
from .crud_cancellation import cancellation
from .base import CRUDBase
from app.models.models import ProductRawRelation, RawRemainsDetail, RawUsageStandards, \
    OrdersProductsRawRelation, OrdersProductsRelation, Permissions
from app.schemas import ProductRawRelationCreate, ProductRawRelationUpdate, RawRemainsDetailCreate, \
    RawRemainsDetailUpdate, RawUsageStandardsCreate, RawUsageStandardsUpdate, OrdersProductsRawRelationCreate, \
    OrdersProductsRawRelationUpdate, OrdersProductsRelationCreate, OrdersProductsRelationUpdate, \
    PermissionsCreate, PermissionsUpdate

raw_usage_standards = CRUDBase[RawUsageStandards, RawUsageStandardsCreate, RawUsageStandardsUpdate](RawUsageStandards)
raw_remains_detail = CRUDBase[RawRemainsDetail, RawRemainsDetailCreate, RawRemainsDetailUpdate](RawRemainsDetail)
product_raw_relation = CRUDBase[ProductRawRelation, ProductRawRelationCreate, ProductRawRelationUpdate](
    ProductRawRelation)
order_product_raw = CRUDBase[OrdersProductsRawRelation, OrdersProductsRawRelationCreate,
                             OrdersProductsRawRelationUpdate](OrdersProductsRawRelation)
order_product = CRUDBase[OrdersProductsRelation, OrdersProductsRelationCreate, OrdersProductsRelationUpdate](
    OrdersProductsRelation)
permissions = CRUDBase[Permissions, PermissionsCreate, PermissionsUpdate](Permissions)

# product = CRUDBase[Product, ProductCreate, ProductUpdate](Product)

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
