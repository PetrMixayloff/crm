import secrets

from app import crud, schemas
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import Any, Dict, Union, List
from app.api import deps
from app.models import models
from app.utils import upload_image_to_aws

router = APIRouter()


@router.post("/", response_model=schemas.File)
def upload_file(file: UploadFile = File(...),
                current_user: models.User = Depends(deps.get_current_active_user),
                db: Session = Depends(deps.get_db)
                ) -> Any:
    """
    Upload file.
    """
    file_ext = file.filename[-4:]
    if file_ext not in ['.jpg', '.png']:
        raise HTTPException(
            status_code=400,
            detail="Not valid file extension.",
        )
    file_name = secrets.token_urlsafe(16) + file_ext
    if not upload_image_to_aws(upload_file=file, file_name=file_name):
        raise HTTPException(
            status_code=500,
            detail="Error while upload file to cloud.",
        )
    file_in = schemas.FileCreate(path=file_name)
    file = crud.file.create(db, obj_in=file_in)
    return file
