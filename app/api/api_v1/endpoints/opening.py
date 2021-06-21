from app import crud, schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models import models


router = APIRouter()


@router.get("/", response_model=schemas.OpeningResponse)
def read_openings(db: Session = Depends(deps.get_db),
                  current_user: models.User = Depends(deps.get_current_active_user),
                  skip: int = 0,
                  take: int = 100,
                  filter: str = None
                  ) -> schemas.OpeningResponse:
    """
    Получение списка документов разборки для магазина.
    """
    shop_id = str(current_user.shop_id)
    return crud.opening.get_multi(db, shop_id=shop_id, skip=skip, take=take, filter=filter)


@router.get("/{opening_id}", response_model=schemas.Opening)
def read_opening_by_id(opening_id: str,
                       db: Session = Depends(deps.get_db),
                       current_user: models.User = Depends(deps.get_current_active_user)
                       ) -> schemas.Opening:
    """
    Получение документа разборки по id.
    """
    opening = crud.invoice.get(db, id=opening_id)
    return opening


@router.post("/", response_model=schemas.Opening)
def create_opening(opening_in: schemas.OpeningCreate,
                   db: Session = Depends(deps.get_db),
                   current_user: models.User = Depends(deps.get_current_active_user),
                   ) -> schemas.Opening:
    """
    Создание нового документа разборки.
    """
    opening = crud.opening.create_opening(db, obj_in=opening_in)
    return opening
