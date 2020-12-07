from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=Dict[str, Union[int, List[schemas.Invoice]]])
def read_invoice_by_shop_id(*, db: Session = Depends(deps.get_db),
                            current_user: models.User = Depends(deps.get_current_active_user),
                            skip: int = 0,
                            take: int = 100,
                            filter: str = None
                            ) -> Any:
    """
    Get Invoice by shop id.
    """
    shop_id = str(current_user.shop_id)
    invoice = crud.invoice.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)
    return invoice


@router.get("/{invoice_id}", response_model=schemas.Invoice)
def read_invoice_by_id(*, db: Session = Depends(deps.get_db),
                       current_user: models.User = Depends(deps.get_current_active_user),
                       invoice_id: str) -> Any:
    """
    Get current invoice by id.
    """
    invoice = crud.invoice.get(db, id=invoice_id)
    return invoice


@router.post("/", response_model=schemas.Invoice)
def create_invoice(*, db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   invoice_in: schemas.InvoiceCreate) -> Any:
    """
    Create new invoice.
    """
    invoice = crud.invoice.create_invoice(db, obj_in=invoice_in,
                                          invoice_record_create=invoice_record_create,
                                          raw_remains_create=raw_remains_create)
    return invoice


@router.put("/{invoice_id}", response_model=schemas.Invoice)
def update_invoice(*, db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   invoice_record_update: List[schemas.InvoiceRecordUpdate],
                   raw_remains_update: List[schemas.RawRemainsDetailUpdate],
                   invoice_update_in: schemas.InvoiceUpdate) -> Any:
    """
    Update invoice.
    """
    invoice = crud.invoice.get(db, id=invoice_update_in.id)
    invoice = crud.invoice.update_invoice(db, obj_in=invoice_update_in, db_obj=invoice,
                                          invoice_record_update=invoice_record_update,
                                          raw_remains_update=raw_remains_update)
    return invoice


@router.delete("/{invoice_id}", response_model=schemas.Invoice)
def delete_invoice(*, db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   invoice_id: str) -> Any:
    """
    Delete invoice.
    """
    invoice = crud.invoice.remove(db, id=invoice_id)
    return invoice
