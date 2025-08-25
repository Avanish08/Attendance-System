from werkzeug.security import generate_password_hash
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://akdis0302:B1xvoFJIp6V88PrS@cluster0.ydzfxbm.mongodb.net/")
db = client["attendance_db"]
users_col = db["users"]


users = [
    {
        "username": "superadmin",
        "password": generate_password_hash("admin123"),  
        "role": "super_admin"   
    },
    {
        "username": "Vimeetadmin",
        "password": generate_password_hash("Vimeet123"),  
        "role": "admin"
    }
]

for u in users:
    if not users_col.find_one({"username": u["username"]}):
        users_col.insert_one(u)
        print(f"User {u['username']} created.")
    else:
        print(f"User {u['username']} already exists.")
