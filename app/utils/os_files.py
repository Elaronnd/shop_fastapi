from PIL import Image, ImageOps
from io import BytesIO
import os

def save_image(
    img: bytes,
    path_file: str
) -> None:
    img = Image.open(BytesIO(img)).convert("RGB")
    ImageOps.cover(img, size=(512, 512)).save(path_file, "webp", quality=75)


def remove_image_file(path_file: str) -> None:
    os.remove(path_file)
