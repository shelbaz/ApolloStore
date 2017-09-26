from project.models.auth_model import User

def get_all_users():
    return User.query_filtered_by()