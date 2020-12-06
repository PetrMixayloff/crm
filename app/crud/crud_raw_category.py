from typing import Dict, Union, Any, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.crud import raw
from app.models.models import RawCategory
from app.schemas import RawCategoryCreate, RawCategoryUpdate


class CRUDRawCategory(CRUDBase[RawCategory, RawCategoryCreate, RawCategoryUpdate]):

    def recursive_disable(self, db: Session, id: str) -> List[RawCategory]:
        deleted_objects = []
        obj = db.query(self.model).get(id)
        deleted_objects.append(obj)
        deleted_objects.extend(self.get_daughter_objects(db, id))
        for obj in deleted_objects:
            obj.is_active = False
            db.add(obj)
            nested_raw = raw.get_multi_by_category_id(db=db, category_id=str(obj.id))
            for obj in nested_raw['data']:
                obj.is_active = False
                db.add(obj)
        db.commit()
        return deleted_objects


raw_category = CRUDRawCategory(RawCategory)
