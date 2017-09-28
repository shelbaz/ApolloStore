from project.models.auth_model import User
from project.models.item_model import Item

def get_all_users():
    return User.query_filtered_by()

def get_all_items():
    return Item.query_filtered_by()