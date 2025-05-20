from app.db.queries.products import (
    get_all_products_filtered,
    get_product_by_id,
    add_product,
    remove_product
)
from app.db.queries.users import (
    is_email_in_db,
    register_user,
    get_password_by_username,
    get_user_by_username,
    get_user_by_id,
    add_product_user,
    remove_product_user
)