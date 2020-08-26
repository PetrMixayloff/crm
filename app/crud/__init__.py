from .crud_user import user
from .base import CRUDBase
from app.models.models import Shop, ProductCategory, Product, File
from app.schemas import ShopCreate, ShopUpdate, ProductCategoryCreate, \
    ProductCategoryUpdate, ProductCreate, ProductUpdate, FileCreate, FileUpdate


shop = CRUDBase[Shop, ShopCreate, ShopUpdate](Shop)
product_category = CRUDBase[ProductCategory, ProductCategoryCreate, ProductCategoryUpdate](ProductCategory)
product = CRUDBase[Product, ProductCreate, ProductUpdate](Product)
file = CRUDBase[File, FileCreate, FileUpdate](File)

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
