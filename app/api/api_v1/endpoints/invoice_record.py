from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.InvoiceRecord]]])
def read_invoice_record_by_shop_id(*, db: Session = Depends(deps.get_db),
                                   current_user: models.User = Depends(deps.get_current_active_user),
                                   skip: int = 0,
                                   take: int = 100,
                                   filter: str = None) -> Any:

    """
    Get InvoiceRecord by shop id.
    """
    shop_id = str(current_user.shop_id)
    invoice_record = crud.invoice_record.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return invoice_record


@router.post("/", response_model=schemas.InvoiceRecord)
def create_invoice_record(*, db: Session = Depends(deps.get_db),
                          current_user: models.User = Depends(deps.get_current_active_user),
                          invoice_record_in: schemas.InvoiceRecordCreate,
                          raw_remains_create: List[schemas.RawRemainsDetailCreate]
                          ) -> Any:
    """
    Create new invoice_record.
    """
    invoice_record = crud.invoice_record.create_invoice_record(db, obj_in=invoice_record_in,
                                                               raw_remains_create=raw_remains_create)
    return invoice_record


@router.put("/{invoice_record_id}", response_model=schemas.InvoiceRecord)
def update_invoice_record(*, db: Session = Depends(deps.get_db),
                          current_user: models.User = Depends(deps.get_current_active_user),
                          invoice_record_update_in: schemas.InvoiceRecordUpdate,
                          raw_remains_update: List[schemas.RawRemainsDetailUpdate]
                          ) -> Any:
    """
    Update invoice record.
    """
    invoice_record = crud.invoice_record.get(db, id=invoice_record_update_in.id)
    invoice_record = crud.invoice_record.update_invoice_record(db, obj_in=invoice_record_update_in,
                                                               db_obj=invoice_record,
                                                               raw_remains_update=raw_remains_update)
    return invoice_record


# @router.delete("/{invoice_record_id}", response_model=schemas.InvoiceRecord)
# def delete_invoice_record(*, db: Session = Depends(deps.get_db),
#                           current_user: models.User = Depends(deps.get_current_active_user),
#                           invoice_record_id: str) -> Any:
#     """
#     Delete invoice record.
#     """
#     invoice_record = crud.invoice_record.remove(db, id=invoice_record_id)
#     return invoice_record
