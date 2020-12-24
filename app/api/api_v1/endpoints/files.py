import secrets
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from typing import Any, Tuple
from app.api import deps
from app.models import models
from app.utils import upload_image_to_aws, delete_image_from_aws, get_presigned_url

router = APIRouter()


@router.post("/")
def upload_file(file_name: str, file_type: str,
                current_user: models.User = Depends(deps.get_current_active_user)
                ) -> str:
    """
    Upload file.
    """
    # file_ext = file.filename[-4:]
    # if file_ext.lower() not in ['.jpg', '.png']:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Not valid file extension.",
    #     )
    # file_name = secrets.token_urlsafe(16) + file_ext
    try:
        response = get_presigned_url(file_name=file_name, file_type=file_type)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error while upload file to cloud.",
        )
    return response


@router.delete("/{file_name}")
def delete_file(file_name: str, current_user: models.User = Depends(deps.get_current_active_user)) -> str:
    """
    Delete file.
    """
    if not delete_image_from_aws(file_name):
        raise HTTPException(
            status_code=500,
            detail="Error while delete file in cloud.",
        )
    return 'ok'
