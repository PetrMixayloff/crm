import copy
import json
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, ColumnProperty, Query
from sqlalchemy.sql import sqltypes
from sqlalchemy import cast, String, desc

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, shop_id: str, skip: int = 0, take: int = 1000000, sort: Union[str, list] = None,
                  filter: Union[str, list] = None) -> Dict[str, Union[int, Any]]:
        objects = db.query(self.model).filter(self.model.is_active.is_(True),
                                              self.model.shop_id == shop_id)
        if filter is not None:
            objects = self.filter_query(objects, filter)

        if sort is not None and isinstance(sort, str):
            objects = self.sort_query(objects, sort)

        total = objects.count()
        objects = objects.offset(skip).limit(take).all()
        data = {
            'totalCount': total,
            'data': objects
        }
        return data

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: str) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def disable(self, db: Session, *, id: str) -> ModelType:
        obj = db.query(self.model).get(id)
        obj.is_active = False
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get_daughter_objects(self, db: Session, id: str) -> List[ModelType]:
        daughter_objects = []
        daughters = db.query(self.model).filter(self.model.parent_id == id).all()
        for daughter in daughters:
            daughter_objects.extend(self.get_daughter_objects(db, str(daughter.id)))
        daughter_objects.extend(daughters)
        return daughter_objects

    def filter_query(self, _query: Query, _filter: Union[str, list]):
        """
        разбор filter expression DevExpress Grid и фильтрация выборки
        :param _query: модифицируемый запрос (объект Query)
        :param _filter: filter expression DevExpress Grid
        :return: модифицированный запрос (объект Query)
        """

        filter_ = json.loads(_filter) if isinstance(_filter, str) else _filter
        query_mod = self.add_filter(_query, filter_)

        return query_mod

    def add_filter(self, _query: Query, _filter: list):
        """
        рекурсивный разбор строки фильтра DevExtreme,
        отдельно анализируются левая и правая часть выражения
        :param _query: модифицируемый запрос (объект Query)
        :param _filter: filter expression DevExpress Grid
        :return: модифицированный запрос (объект Query)
        """
        if not isinstance(_filter, list):
            return _query

        if not isinstance(_filter[0], list) and len(_filter) == 3:
            query_mod = self.add_one_filter_condition(_query, _filter)
        else:
            _left_side = _filter[0]
            _operator = _filter[1]
            _right_side = _filter[2]
            # _operator means always be 'and'
            query_mod = self.add_filter(_query, _left_side)
            query_mod = self.add_filter(query_mod, _right_side)

        return query_mod

    def add_one_filter_condition(self, _query: Query, _filter: list):
        """
         анализ подстроки фильтра DevExtreme, в которой не содержится составных выражений
         :param _query: модифицируемый запрос (объект Query)
         :param _filter: строка фильтра, содежащая одно выражение вида [имя поля, правило, значение]
         :return: модифицированный запрос (объект Query)
         """
        if not isinstance(_filter, list):
            return _query

        query_mod = copy.copy(_query)

        _field = _filter[0]
        _rule = _filter[1]
        _value = _filter[2]
        try:
            _attr = getattr(self.model, _field)
        except AttributeError:
            pass
        else:
            attr_ = _attr
            if (_rule == "contains" or _rule == "notcontains" or _rule == "startswith" or _rule == "endswith") and \
                    (type(_attr.property) is not ColumnProperty or not isinstance(_attr.property.columns[0].type,
                                                                                  sqltypes.String)):
                attr_ = cast(_attr, String)

            if _rule == "contains":
                query_mod = query_mod.filter(attr_.ilike("%" + _value + "%"))
            elif _rule == "notcontains":
                query_mod = query_mod.filter(attr_.notilike("%" + _value + "%"))
            elif _rule == "startswith":
                query_mod = query_mod.filter(attr_.ilike(_value + "%"))
            elif _rule == "endswith":
                query_mod = query_mod.filter(attr_.ilike("%" + _value))
            elif _rule == "=":
                query_mod = query_mod.filter(_attr == _value)
            elif _rule == "<>":
                query_mod = query_mod.filter(_attr != _value)
            elif _rule == "in":
                query_mod = query_mod.filter(_attr.in_(_value))
            elif _rule == "not_in":
                query_mod = query_mod.filter(_attr.notin_(_value))
            elif _rule == ">=":
                query_mod = query_mod.filter(_attr >= _value)
            elif _rule == "<":
                query_mod = query_mod.filter(_attr < _value)
        return query_mod

    def sort_query(self, query: Query, sort: str):
        """
        сортировка выборки из базы по sort expression DevExpress Grid
        :param query: модифицируемый запрос (объект Query)
        :param sort: sort expression DevExpress Grid
        :return: модифицированный запрос (объект Query)
        """

        try:
            sort = json.loads(sort)
        except json.decoder.JSONDecodeError:
            return query

        field, desc_rule = None, None
        for sort_rule in sort:
            field = sort_rule.get('selector')
            desc_rule = sort_rule.get('desc')
        if field is None or desc_rule is None:
            return query
        try:
            attr = getattr(self.model, field)
        except AttributeError:
            return query
        if desc_rule:
            return query.order_by(desc(attr))
        return query.order_by(attr)
