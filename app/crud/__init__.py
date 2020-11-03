from .crud_user import user
from .crud_shop import shop
from .crud_product import product
from .base import CRUDBase
from app.models.models import ProductCategory, Product, RawCategory, Raw, File
from app.schemas import ProductCategoryCreate, ProductCategoryUpdate, ProductCreate, \
    ProductUpdate, RawCategoryCreate, RawCategoryUpdate, RawCreate, RawUpdate, FileCreate, FileUpdate

raw = CRUDBase[Raw, RawCreate, RawUpdate](Raw)
raw_category = CRUDBase[RawCategory, RawCategoryCreate, RawCategoryUpdate](RawCategory)
product_category = CRUDBase[ProductCategory, ProductCategoryCreate, ProductCategoryUpdate](ProductCategory)
# product = CRUDBase[Product, ProductCreate, ProductUpdate](Product)
file = CRUDBase[File, FileCreate, FileUpdate](File)

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
