Got it 🚀
Here’s a simple but professional **`README.md`** you can put at the root of your project:

---

# 🎓 AIML Department Attendance & Timetable Management

This project is a **desktop-based web app** built with **Flask + MongoDB + PyWebView**, designed for managing students, subjects, attendance, and timetables for the **AIML department** (S.E, T.E, B.E).

---

## ✨ Features

* 🔑 **Authentication** (Admin / Super Admin)
* 👨‍🎓 **Manage Students** (CRUD: Add, Edit, Delete, View)
* 📚 **Manage Subjects** (CRUD for theory & practicals)
* 🗓 **Manage Timetable** (Lecture-wise, 7 lectures per day, CRUD)
* ✅ **Mark Attendance** (0–7 per subject, daily basis)
* 📊 **Show & Edit Attendance** (with totals & percentage column)
* 📥 **Download Attendance Report** (CSV export using Pandas)
* 🖥 **Runs as Desktop App** (via PyWebView, no browser needed)

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/aiml-attendance.git
cd aiml-attendance
```

### 2️⃣ Setup virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirement.txt
```

---

## 🗄 Database Setup

This project uses **MongoDB**.

* Make sure MongoDB is running locally (default: `mongodb://localhost:27017/`)
* The database name and collections are configured in `utils/mongo_config.py`.
* Collections used:

  * `users` (for login)
  * `students`
  * `subjects`
  * `timetable`
  * `attendance`

To create an **admin user**:

```python
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient("mongodb://localhost:27017/")
db = client["aiml_db"]
users = db["users"]

users.insert_one({
    "username": "admin",
    "password": generate_password_hash("admin123"),
    "role": "super_admin"
})
```

---

## 🚀 Running the App

Run the Flask app:

```bash
python app.py
```

If **PyWebView** is installed, it will open as a **desktop window**.
Otherwise, open manually in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📦 Building EXE (Windows)

You can bundle the app as a desktop `.exe` using **PyInstaller**:

```bash
pyinstaller --noconsole --onefile --add-data "templates;templates" --add-data "static;static" app.py
```

Output will be inside the `dist/` folder.

---

## 📌 Project Structure

```
.
├── app.py                # Main application
├── requirements.txt      # Python dependencies
├── templates/            # HTML files
│   ├── login.html
│   ├── dashboard.html
│   ├── manage_students.html
│   ├── manage_subjects.html
│   ├── mark_attendance.html
│   ├── show_attendance.html
│   ├── add_timetable.html
│   └── show_timetable.html
├── static/               # CSS/JS files (if any)
└── utils/                # Helper modules
    ├── auth.py
    └── mongo_config.py
```

---

## 🛠 Tech Stack

* **Backend:** Flask
* **Database:** MongoDB
* **Frontend:** HTML, Bootstrap (via Flask templates)
* **Desktop Wrapper:** PyWebView

---

## 🙌 Author

Developed for **Avanish Ojha** attendance and timetable automation.

---


