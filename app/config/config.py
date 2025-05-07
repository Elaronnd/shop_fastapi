from yaml import safe_load

with open("app/config/config.yml", "r") as file:
    config_data = safe_load(file)

SECRET_KEY = config_data["secret_key"]
ALGORITHM = config_data["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = config_data["access_token_expire_minutes"]
AUTH_NGROK = config_data["auth_ngrok"]
STATUS_CODE = {
    "user not found": 404,
    "user already exists": 409,
    "this email already registered": 409
}
