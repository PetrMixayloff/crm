from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=schemas.InvoicesResponse)
def read_invoices(db: Session = Depends(deps.get_db),
                  current_user: models.User = Depends(deps.get_current_active_user),
                  skip: int = 0,
                  take: int = 100,
                  filter: str = None
                  ) -> schemas.InvoicesResponse:
    """
    Получение списка приходных накладных для магазина.
    """
    shop_id = str(current_user.shop_id)
    return crud.invoice.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)


@router.get("/{invoice_id}", response_model=schemas.Invoice)
def read_invoice_by_id(invoice_id: str,
                       db: Session = Depends(deps.get_db),
                       current_user: models.User = Depends(deps.get_current_active_user)
                       ) -> schemas.Invoice:
    """
    Получение приходной накладной по id.
    """
    invoice = crud.invoice.get(db, id=invoice_id)
    return invoice


@router.post("/", response_model=schemas.Invoice)
def create_invoice(invoice_in: schemas.InvoiceCreate,
                   db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   ) -> schemas.Invoice:
    """
    Создание новой приходной накладной.
    """
    invoice = crud.invoice.create_invoice(db, obj_in=invoice_in)
    return invoice
