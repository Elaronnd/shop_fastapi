import os
import json
from io import BytesIO
from typing import Optional, Union
from uuid import uuid4
from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, Request, BackgroundTasks, HTTPException
from fastapi.params import File, Form, Query, Path
from fastapi.responses import Response
from app.db.models.product import Product
from app.db.queries import get_user_by_username, remove_product_user
from app.db.queries.products import add_product, remove_product, get_all_products_filtered, get_product_by_id
from app.utils.jwt_user import get_current_user
from app.utils.os_files import save_image, remove_image_file
from app.validation.pydantic_classes import (
    ProductData,
    ProductResponse,
    UserData
)
from app.config.config import (
    IMAGES_PATH,
    DEFAULT_CATEGORY,
    IMAGES_FORMAT,
    STATUS_CODE
)

product_router = APIRouter()


def product_form_parser(
        title: str = Form(..., title="Title", description="Title of product", min_length=2, max_length=35),
        description: str = Form(..., title="Description", description="Description of product", min_length=10,
                                 max_length=1000),
        price: int = Form(..., title="Price", description="Price of product", le=1000000),
        category_id: int = Form(..., title="Category id", description="Id of category title", le=len(DEFAULT_CATEGORY))
) -> Product:
    return Product(title=title, description=description, price=price, category_id=category_id)


@product_router.get("/products", status_code=200, response_model=list[ProductResponse], tags=["v1/products"])
async def all_products(
    request: Request,
    min_price: int = Query(default=0, title="Min price", description="Min price of product", le=1000000),
    max_price: int = Query(default=1000000, title="Max price", description="Max price of product", le=1000000),
    category_id: Union[int, None] = Query(default=None, title="Category id", description="Id of category title", le=len(DEFAULT_CATEGORY))
):
    products = get_all_products_filtered(
        min_price=min_price,
        max_price=max_price,
        category_id=category_id
    )
    list_products = []

    for product in products:
        try:
            images = [f"https://{request.url.hostname}/image/{os.path.basename(images_name)}" for images_name in
                      product.images]
        except TypeError:
            images = []
        list_products.append(
            ProductResponse(
                id=product.id,
                title=product.title,
                description=product.description,
                price=product.price,
                images=images,
                category_id=product.category_id
            )
        )
    return list_products


@product_router.post("/product", status_code=202, response_model=ProductResponse, tags=["v1/products"])
async def create_product(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: UserData = Depends(get_current_user),
    details: ProductData = Depends(product_form_parser),
    images: Optional[list[UploadFile]] = File(default=None, title="Your images", description="If you want you can upload images of your product"),
):
    user_images_path = []
    if images is not None:
        for image in images:
            if not image.filename.lower().endswith(IMAGES_FORMAT):
                raise HTTPException(status_code=406, detail=f"\"{image.filename}\" is not image")
            elif image.size > 5000000:
                raise HTTPException(status_code=413, detail=f"Image \"{image.filename}\" is too large")
            elif len(images) > 5:
                raise HTTPException(status_code=413, detail="You can upload up to 5 images")
            img = await image.read()
            width, height = Image.open(BytesIO(img)).size
            if width < 512 or height < 512:
                raise HTTPException(status_code=413,
                                    detail=f"Image \"{image.filename}\" resolution does not correspond to 512x512")
            image.file.seek(0)
            path_file = IMAGES_PATH + uuid4().hex + ".webp"
            background_tasks.add_task(save_image, img=img, path_file=path_file)
            user_images_path.append(path_file)

    user_images_path = None if user_images_path == [] else user_images_path
    user_id = get_user_by_username(username=current_user.username).get("id")

    try:
        product = add_product(
            title=details.title,
            description=details.description,
            price=details.price,
            images=json.dumps(user_images_path),
            category_id=details.category_id,
            user_id=user_id
        )
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))

    try:
        user_images_path = [
            (
                f"{request.url.scheme}://{request.url.hostname}"
                f"{'' if request.url.port in [80, 443] else f':{request.url.port}'}"
                f"/image/{os.path.basename(path)}"
            )
            for path in user_images_path
        ]
    except TypeError:
        user_images_path = []

    return ProductResponse(
        id=product.id,
        title=details.title,
        description=details.description,
        price=details.price,
        images=user_images_path,
        category_id=details.category_id
    )


@product_router.delete("/product/{product_id}", tags=["v1/products"])
async def delete_product(
    background_tasks: BackgroundTasks,
    product_id: int = Path(..., title="Product id", description="Id of product in db"),
    current_user: UserData = Depends(get_current_user),
):
    user_id = get_user_by_username(username=current_user.username).get("id")
    try:
        product_info = remove_product(
            product_id=product_id,
            user_id=user_id
        )
        remove_product_user(
            product_id=product_id,
            user_id=user_id
        )
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))

    try:
        for image in product_info.get("images"):
            background_tasks.add_task(remove_image_file, path_file=image)
    except TypeError:
        pass

    return Response(status_code=204, background=background_tasks)


@product_router.get("/product/{product_id}", response_model=ProductResponse, tags=["v1/products"])
async def get_product(
    request: Request,
    product_id: int = Path(..., title="Product id", description="Id of product in db")
):
    try:
        product = get_product_by_id(
            product_id=product_id
        )
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))

    return ProductResponse(
        id=product.id,
        title=product.title,
        description=product.description,
        price=product.price,
        images=[f"{request.url.scheme}://{request.url.hostname}{'' if request.url.port in [80, 443] else f':{request.url.port}'}/image/{os.path.basename(images_name)}" for images_name in product.images],
        category_id=product.category_id
    )
