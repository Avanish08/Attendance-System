from pymongo import MongoClient

client = MongoClient("mongodb+srv://akdis0302:B1xvoFJIp6V88PrS@cluster0.ydzfxbm.mongodb.net/")
db = client["attendance_db"]
students_col = db["students"]
attendance_col = db["attendance"]
users_col = db["users"]
timetables_col = db["timetables"]
subjects_col = db["subjects"]

