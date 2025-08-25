from werkzeug.security import generate_password_hash
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("YOUR MONGO DB ADDRESS")
db = client["attendance_db"]
users_col = db["users"]


users = [
    {
        "username": "superadmin",
        "password": generate_password_hash("admin123"),  
        "role": "super_admin"   
    },
    {
        "username": "admin",
        "password": generate_password_hash("admin@123"),  
        "role": "admin"
    }
]

for u in users:
    if not users_col.find_one({"username": u["username"]}):
        users_col.insert_one(u)
        print(f"User {u['username']} created.")
    else:
        print(f"User {u['username']} already exists.")

