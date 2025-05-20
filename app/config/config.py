from yaml import safe_load

with open("app/config/config.yml", "r", encoding="utf-8") as file:
    config_data = safe_load(file)

SECRET_KEY = config_data["secret_key"]
ALGORITHM = "HS256"
AUTH_NGROK = config_data["auth_ngrok"]
ACCESS_TOKEN_EXPIRE_MINUTES = 30
IMAGES_PATH = "app/static/images/"
DEFAULT_CATEGORY = [
    "Ноутбуки та комп’ютери",
    "Смартфони, ТВ і електроніка",
    "Товари для геймерів",
    "Побутова техніка",
    "Товари для дому"
]
TAGS_METADATA = [
    {
        "name": "v1/user",
        "description": "Operations with **users**.",
    },
    {
        "name": "v1/products",
        "description": "Operations with **products**.",
    },
    {
        "name": "v1/image",
        "description": "Operations with **image**.",
    },
]
FORBIDDEN_TAGS = ("(seller)", "(system)")
STATUS_CODE = {
    "user not found": 404,
    "user already exists": 409,
    "this email already registered": 409,
    "invalid price": 400,
    "invalid category_id": 400,
    "unknown product_id": 404,
    "product not found": 404,
    "you do not have permission to perform this action": 403
}
STATUS_CODE_WEBSOCKET = {
    "user not found": 1008
}
IMAGES_FORMAT = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
)
