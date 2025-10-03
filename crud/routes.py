from flask import Blueprint, render_template, request, redirect
from db import get_connection

# Create a blueprint
main_routes = Blueprint('main_routes', __name__)

# Home - List all students
@main_routes.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template("index.html", students=students)

# Add student
@main_routes.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, email, age) VALUES (%s, %s, %s)",
            (name, email, age)
        )
        conn.commit()
        conn.close()
        return redirect("/?success=1")
    return render_template("add.html")


# Edit student
@main_routes.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]
        cursor.execute(
            "UPDATE students SET name=%s, email=%s, age=%s WHERE id=%s",
            (name, email, age, id)
        )
        conn.commit()
        conn.close()
        return redirect("/?success=1")

    # GET request: fetch student data
    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    conn.close()

    return render_template("edit.html", student=student)


# Delete student
@main_routes.route("/delete/<int:id>")
def delete_student(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect("/")
