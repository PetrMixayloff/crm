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
    invoice = crud.invoice.create(db, obj_in=invoice_in)
    return invoice


@router.put("/{invoice_id}", response_model=schemas.Invoice)
def update_invoice(*, db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   invoice_update_in: schemas.InvoiceUpdate) -> Any:
    """
    Update invoice.
    """
    invoice = crud.invoice.get(db, id=invoice_update_in.id)
    invoice = crud.invoice.update(db, obj_in=invoice_update_in, db_obj=invoice)
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
