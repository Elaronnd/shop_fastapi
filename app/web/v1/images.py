from os.path import exists, basename
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.db.queries import get_user_by_username
from app.utils.jwt_user import get_current_user
from app.utils.os_files import remove_image_file
from app.validation.pydantic_classes import UserData
from fastapi.responses import FileResponse, Response

images_router = APIRouter()

@images_router.get("/images/{filename}", response_class=FileResponse, tags=["v1/image"])
async def read_image(
    filename: str
):
    if not exists(f"app/static/images/{filename}"):
        raise HTTPException(status_code=404, detail="Not found")
    return f"app/static/images/{filename}"


@images_router.delete("/images/{filename}", tags=["v1/image"])
async def delete_image(
    filename: str,
    background_tasks: BackgroundTasks,
    current_user: UserData = Depends(get_current_user)
):
    if not exists(f"app/static/images/{filename}"):
        raise HTTPException(status_code=404, detail="Not found")
    elif not any(basename(path_file).name == filename for path_file in get_user_by_username(username=current_user.username).get("products", [])):
        raise HTTPException(status_code=403, detail="You're not the owner of these files")
    background_tasks.add_task(remove_image_file, path_file=f"app/static/images/{filename}")
    return Response(status_code=204, background=background_tasks)
