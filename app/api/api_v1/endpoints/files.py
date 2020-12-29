from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.api import deps
from app.models import models
from app.utils import delete_image_from_aws, get_presigned_url

router = APIRouter()


@router.post("/")
def upload_file(file_name: str, file_type: str,
                current_user: models.User = Depends(deps.get_current_active_user)
                ) -> str:
    """
    Upload file.
    """
    try:
        response = get_presigned_url(file_name=file_name, file_type=file_type)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error while upload file to cloud.",
        )
    return response


@router.delete("/{file_name}")
def delete_file(file_name: str,
                background_tasks: BackgroundTasks,
                current_user: models.User = Depends(deps.get_current_active_user)) -> str:
    """
    Delete file.
    """
    background_tasks.add_task(delete_image_from_aws, file_name)
    # if not delete_image_from_aws(file_name):
    #     raise HTTPException(
    #         status_code=500,
    #         detail="Error while delete file in cloud.",
    #     )
    return 'ok'
