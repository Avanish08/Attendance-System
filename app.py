from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_user, logout_user, login_required, current_user
from utils.auth import login_manager, User, verify_password
from utils.mongo_config import users_col, db
from bson.objectid import ObjectId
import datetime
import pandas as pd
import webbrowser
from threading import Timer
import io
from flask import Response
import webview   
app = Flask(__name__)
app.secret_key = "super_secret_key"

# Initialize login manager
login_manager.init_app(app)
login_manager.login_view = "login"  

# ========== Auth ==========
@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_dict = users_col.find_one({"username": username})
        if user_dict and verify_password(user_dict["password"], password):
            user = User(user_dict)
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ========== Dashboard ==========
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username, role=current_user.role)


# ========== Students (CRUD) ==========
@app.route("/student/manage", methods=["GET", "POST"])
@login_required
def manage_students():
    if current_user.role not in ["admin", "super_admin"]:
        return "Unauthorized", 403

    if request.method == "POST":
        db.students.insert_one({
            "rollno": request.form["rollno"],
            "name": request.form["name"],
            "year": request.form["year"],
            "department": request.form["department"]
        })
        flash("Student added successfully!", "success")
        return redirect(url_for("manage_students"))

    students = list(db.students.find())
    return render_template("manage_students.html", students=students)


@app.route("/student/delete/<id>")
@login_required
def delete_student(id):
    if current_user.role not in ["admin", "super_admin"]:
        return "Unauthorized", 403
    db.students.delete_one({"_id": ObjectId(id)})
    flash("Student deleted!", "success")
    return redirect(url_for("manage_students"))


# ========== Subjects (CRUD) ==========
@app.route("/subject/manage", methods=["GET", "POST"])
@login_required
def manage_subjects():
    if current_user.role not in ["admin", "super_admin"]:
        return "Unauthorized", 403

    if request.method == "POST":
        db.subjects.insert_one({
            "subject_name": request.form["subject_name"],
            "type": request.form["type"],
            "year": request.form["year"],
            "department": request.form["department"]
        })
        flash("Subject added successfully!", "success")
        return redirect(url_for("manage_subjects"))

    subjects = list(db.subjects.find())
    return render_template("manage_subjects.html", subjects=subjects)


@app.route("/subject/delete/<id>")
@login_required
def delete_subject(id):
    if current_user.role not in ["admin", "super_admin"]:
        return "Unauthorized", 403
    db.subjects.delete_one({"_id": ObjectId(id)})
    flash("Subject deleted!", "success")
    return redirect(url_for("manage_subjects"))



# ---------------- TIME TABLE ----------------

@app.route("/timetable", methods=["GET"])
@login_required
def show_timetable():
    if current_user.role not in ["admin", "super_admin", "superadmin"]:
        return "Unauthorized", 403

    dept = request.args.get("department", "AIML")
    year = request.args.get("year", "SE")

    timetable = list(db.timetable.find({"department": dept, "year": year}))
    return render_template("show_timetable.html", timetable=timetable,
                           department=dept, year=year)


@app.route("/timetable/add", methods=["GET", "POST"])
@login_required
def add_timetable():
    if current_user.role not in ["admin", "super_admin", "superadmin"]:
        return "Unauthorized", 403

    if request.method == "POST":
        dept = request.form["department"]
        year = request.form["year"]
        day = request.form["day"]

        lectures = []
        for i in range(1, 8):  # 7 lectures
            lectures.append(request.form.get(f"lec{i}", ""))

        db.timetable.update_one(
            {"department": dept, "year": year, "day": day},
            {"$set": {"lectures": lectures}},
            upsert=True
        )

        flash("Timetable saved successfully!", "success")
        return redirect(url_for("show_timetable", department=dept, year=year))

    return render_template("add_timetable.html")




@app.route("/timetable/view")
@login_required
def view_timetable():
    timetables = list(db.timetable.find())
    return render_template("show_timetable.html", timetables=timetables)


@app.route("/timetable/delete/<id>")
@login_required
def delete_timetable(id):
    if current_user.role not in ["admin", "super_admin"]:
        return "Unauthorized", 403
    db.timetable.delete_one({"_id": ObjectId(id)})
    flash("Timetable deleted!", "success")
    return redirect(url_for("add_timetable"))


# ========== Attendance ==========
@app.route("/attendance/mark", methods=["GET", "POST"])
@login_required
def mark_attendance():
    if current_user.role not in ["admin", "super_admin", "superadmin"]:
        return "Unauthorized", 403

  
    dept = request.values.get("department", "AIML")
    year = request.values.get("year", "SE")


    students_cur = db.students.find({"department": dept, "year": year}).sort("rollno", 1)
    subjects_cur = db.subjects.find({"department": dept, "year": year}).sort("subject_name", 1)

    students = [{"_id": str(s["_id"]), "rollno": s.get("rollno", ""), "name": s.get("name", "")}
                for s in students_cur]
    subjects = [{"_id": str(x["_id"]), "subject_name": x.get("subject_name", ""),
                 "type": x.get("type", "theory")}
                for x in subjects_cur]

    if request.method == "POST":
     
        student_ids = request.form.getlist("student_ids[]")
        today = datetime.date.today().isoformat()

        for sid in student_ids:
            marks = {}
            total = 0
            for sub in subjects:
                key = f"{sid}__{sub['_id']}"  
                val = int(request.form.get(key, 0) or 0)
                # clamp to 0..7
                if val < 0: val = 0
                if val > 7: val = 7
                marks[sub["_id"]] = val
                total += val

            db.attendance.insert_one({
                "student_id": ObjectId(sid),
                "department": dept,
                "year": year,
                "date": today,
                "marks": marks,  
                "total": total
            })

        flash("Attendance saved.", "success")
     
        return redirect(url_for("mark_attendance", department=dept, year=year))

    return render_template(
        "mark_attendance.html",
        students=students,
        subjects=subjects,
        department=dept,
        year=year
    )




@app.route("/attendance/view", methods=["GET", "POST"])
@login_required
def show_attendance():
    from utils.mongo_config import students_col, attendance_col, subjects_col
    from datetime import datetime

    if current_user.role not in ["admin", "super_admin"]:
        return "Unauthorized", 403

    department = "AIML"  # hardcoded
    year = request.args.get("year", "SE")
    date = request.args.get("date", datetime.today().strftime("%Y-%m-%d"))

    if request.method == "POST":
        student_ids = request.form.getlist("student_ids[]")

        for sid in student_ids:
            record = {}
         
            for sub in subjects_col.find({"department": department, "year": year}):
                sub_id = str(sub["_id"])
                marks = int(request.form.get(f"{sub_id}_{sid}", 0))
                record[sub["subject_name"]] = marks

            record["total"] = sum(record.values())
            record["percentage"] = round((record["total"] / (len(record) * 7)) * 100, 2)
            record.update({
                "student_id": sid,
                "department": department,
                "year": year,
                "date": date
            })

            attendance_col.update_one(
                {"student_id": sid, "department": department, "year": year, "date": date},
                {"$set": record},
                upsert=True
            )

        flash("✅ Attendance updated successfully!", "success")
        return redirect(url_for("show_attendance", year=year, date=date))


    subjects = list(subjects_col.find({"department": department, "year": year}))
    students = list(students_col.find({"department": department, "year": year}))
    records_db = list(attendance_col.find({"department": department, "year": year, "date": date}))

    # Merge student info with attendance
    records = []
    for s in students:
        rec = next((r for r in records_db if str(r["student_id"]) == str(s["_id"])), {})
        merged = {"student_id": str(s["_id"]), "rollno": s["rollno"], "name": s["name"]}
        merged.update(rec)
        records.append(merged)

    return render_template("show_attendance.html",
                           subjects=subjects,
                           records=records,
                           year=year,
                           date=date)


@app.route("/attendance/report")
@login_required
def attendance_report():
    from utils.mongo_config import attendance_col, subjects_col, students_col

    department = request.args.get("department", "AIML")
    year = request.args.get("year", "SE")

    subjects = list(subjects_col.find({"department": department, "year": year}))
    students = list(students_col.find({"department": department, "year": year}))
    records = list(attendance_col.find({"department": department, "year": year}))

 
    data = []
    for s in students:
        rec = next((r for r in records if str(r["student_id"]) == str(s["_id"])), {})
        merged = {"Roll No": s["rollno"], "Name": s["name"]}
        for sub in subjects:
            merged[sub["subject_name"]] = rec.get(sub["subject_name"], 0)
        merged["Total"] = rec.get("total", 0)
        merged["Percentage"] = rec.get("percentage", 0)
        data.append(merged)

    # Export CSV
  

    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=attendance_report.csv"}
    )

# ----------------- DESKTOP ENTRY POINT -----------------

if __name__ == "__main__":
    app.run(debug=True)





