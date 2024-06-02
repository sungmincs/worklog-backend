import os

from fastapi import APIRouter

from worklog.settings import settings

router = APIRouter()


@router.get(
    "",
)
async def healthcheck():
    """
    get health status
    """
    curr_image_tag = os.getenv("IMAGE_TAG", settings.image_tag)
    return {
        "health": "OK",
        "imageTag": curr_image_tag,
    }
