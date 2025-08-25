from flask_login import LoginManager, UserMixin
from werkzeug.security import check_password_hash
from bson.objectid import ObjectId
from .mongo_config import users_col

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, user_dict):
        self.id = str(user_dict["_id"])
        self.username = user_dict["username"]
        self.role = user_dict["role"]

@login_manager.user_loader
def load_user(user_id):
    user_dict = users_col.find_one({"_id": ObjectId(user_id)})
    if user_dict:
        return User(user_dict)
    return None

def verify_password(stored_hash, password):
    return check_password_hash(stored_hash, password)
