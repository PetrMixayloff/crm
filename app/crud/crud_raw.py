from typing import Dict, Union, Any, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Raw
from app.schemas import RawCreate, RawUpdate


class CRUDRaw(CRUDBase[Raw, RawCreate, RawUpdate]):

    def get_multi_by_category_id(
            self, db: Session, category_id: str, skip: int = 0, take: int = 1000000, filter: str = None
    ) -> Dict[str, Union[int, Any]]:
        raws = db.query(self.model).filter(self.model.is_active.is_(True),
                                               self.model.category_id == category_id)
        if filter is not None:
            raws = self.filter_query(raws, filter)
        raws = raws.offset(skip).limit(take).all()
        data = {
            'totalCount': len(raws),
            'data': raws
        }
        return data


raw = CRUDRaw(Raw)
