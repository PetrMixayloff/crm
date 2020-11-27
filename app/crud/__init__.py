from .crud_user import user
from .crud_shop import shop
from .crud_product import product
from .crud_raw import raw
from .crud_invoice_record import invoice_record
from .base import CRUDBase
from app.models.models import ProductCategory, ProductRawRelation, RawCategory, RawRemainsDetail, Client, Invoice
from app.schemas import ProductCategoryCreate, ProductCategoryUpdate, ProductRawRelationCreate, ProductRawRelationUpdate, \
    RawCategoryCreate, RawCategoryUpdate, ClientCreate, ClientUpdate, InvoiceCreate, InvoiceUpdate,RawRemainsDetailCreate,\
    RawRemainsDetailUpdate


raw_remains_detail = CRUDBase[RawRemainsDetail, RawRemainsDetailCreate, RawRemainsDetailUpdate](RawRemainsDetail)
invoice = CRUDBase[Invoice, InvoiceCreate, InvoiceUpdate](Invoice)
product_raw_relation = CRUDBase[ProductRawRelation, ProductRawRelationCreate, ProductRawRelationUpdate](ProductRawRelation)
client = CRUDBase[Client, ClientCreate, ClientUpdate](Client)
raw_category = CRUDBase[RawCategory, RawCategoryCreate, RawCategoryUpdate](RawCategory)
product_category = CRUDBase[ProductCategory, ProductCategoryCreate, ProductCategoryUpdate](ProductCategory)
# product = CRUDBase[Product, ProductCreate, ProductUpdate](Product)

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
