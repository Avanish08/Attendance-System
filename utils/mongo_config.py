from pymongo import MongoClient

client = MongoClient("YOUR MONOGO DB ADDRESS")
db = client["attendance_db"]
students_col = db["students"]
attendance_col = db["attendance"]
users_col = db["users"]
timetables_col = db["timetables"]
subjects_col = db["subjects"]


