from .crud_user import user
from .crud_shop import shop
from .crud_product import product
from .crud_product_category import product_category
from .crud_raw import raw
from .crud_raw_category import raw_category
from .crud_invoice import invoice
from .crud_order import order
from .crud_cancelation import cancelation
from .base import CRUDBase
from app.models.models import ProductCategory, ProductRawRelation, RawCategory, RawRemainsDetail, Client,\
    InvoiceRecord, Inventory, RawUsageStandards, OrdersProductsRawRelation, OrdersProductsRelation, CancelationRecord
from app.schemas import ProductCategoryCreate, ProductCategoryUpdate, ProductRawRelationCreate, ProductRawRelationUpdate, \
    RawCategoryCreate, RawCategoryUpdate, ClientCreate, ClientUpdate, InvoiceRecordUpdate,\
    InvoiceRecordCreate, RawRemainsDetailCreate, RawRemainsDetailUpdate, InventoryCreate,\
    InventoryUpdate, RawUsageStandardsCreate, RawUsageStandardsUpdate, OrdersProductsRawRelationCreate, \
    OrdersProductsRawRelationUpdate, OrdersProductsRelationCreate, OrdersProductsRelationUpdate, \
    OrderCreate, OrderUpdate, CancelationRecordCreate, CancelationRecordUpdate

raw_usage_standards = CRUDBase[RawUsageStandards, RawUsageStandardsCreate, RawUsageStandardsUpdate](RawUsageStandards)
inventory = CRUDBase[Inventory, InventoryCreate, InventoryUpdate](Inventory)
raw_remains_detail = CRUDBase[RawRemainsDetail, RawRemainsDetailCreate, RawRemainsDetailUpdate](RawRemainsDetail)
invoice_record = CRUDBase[InvoiceRecord, InvoiceRecordCreate, InvoiceRecordUpdate](InvoiceRecord)
product_raw_relation = CRUDBase[ProductRawRelation, ProductRawRelationCreate, ProductRawRelationUpdate](ProductRawRelation)
client = CRUDBase[Client, ClientCreate, ClientUpdate](Client)
order_product_raw = CRUDBase[OrdersProductsRawRelation, OrdersProductsRawRelationCreate,
                             OrdersProductsRawRelationUpdate](OrdersProductsRawRelation)
order_product = CRUDBase[OrdersProductsRelation, OrdersProductsRelationCreate, OrdersProductsRelationUpdate]
cancelation_record = CRUDBase[CancelationRecord, CancelationRecordCreate, CancelationRecordUpdate](CancelationRecord)
# product = CRUDBase[Product, ProductCreate, ProductUpdate](Product)

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
