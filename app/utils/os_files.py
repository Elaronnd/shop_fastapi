from PIL import Image, ImageOps
from io import BytesIO
import os

def save_image(
    img: bytes,
    path_file: str
) -> None:
    with Image.open(BytesIO(img)) as img:
        img = ImageOps.exif_transpose(img).convert("RGB")
        resized = ImageOps.fit(img, (512, 512))
        resized.save(path_file, "webp", quality=75)

def remove_image_file(path_file: str) -> None:
    os.remove(path_file)
