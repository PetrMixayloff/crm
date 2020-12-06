from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.crud import product
from app.models.models import ProductCategory
from app.schemas import ProductCategoryCreate, ProductCategoryUpdate


class CRUDProductCategory(CRUDBase[ProductCategory, ProductCategoryCreate, ProductCategoryUpdate]):

    def recursive_disable(self, db: Session, id: str) -> List[ProductCategory]:
        deleted_objects = []
        obj = db.query(self.model).get(id)
        deleted_objects.append(obj)
        deleted_objects.extend(self.get_daughter_objects(db, id))
        for obj in deleted_objects:
            obj.is_active = False
            db.add(obj)
            nested_products = product.get_multi_by_category_id(db=db, category_id=str(obj.id))
            for obj in nested_products['data']:
                obj.is_active = False
                db.add(obj)
        db.commit()
        return deleted_objects


product_category = CRUDProductCategory(ProductCategory)
