from flask import Flask, jsonify, request, render_template
import time, requests, os, json
from jose import jwt
import mysql.connector

ISSUER = os.getenv("OIDC_ISSUER", "http://authentication-identity-server:8080/realms/realm_N08")
ISSUER_AUTH = "http://localhost:8081/realms/realm_N08"
AUDIENCE = os.getenv("OIDC_AUDIENCE", "flask-app")
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
_JWKS = None; _TS = 0
def get_jwks():
    global _JWKS, _TS
    now = time.time()
    if not _JWKS or now - _TS > 600:
        _JWKS = requests.get(JWKS_URL, timeout=5).json()
        _TS = now
    return _JWKS
app = Flask(__name__)
@app.get("/hello")
def hello(): return jsonify(message="Hello from App Server!")
@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    token = auth.split(" ",1)[1]
    try:
        payload = jwt.decode(token, get_jwks(), algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
        return jsonify(message="Secure resource OK", preferred_username=payload.get("preferred_username"))
    except Exception as e:
        return jsonify(error=str(e)), 401
        

        
@app.get("/student")
def student():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "students.json")

    with open(file_path) as f:
        data = json.load(f)

    return render_template("students.html", students=data)
    
######################################

db_config = {
    "host": "relational-database-server",
    "user": "root",
    "password": "root",
    "database": "studentdb"
}

def get_conn():
    return mysql.connector.connect(**db_config)

# Hiển thị danh sách sinh viên
@app.get("/students-db")
def students_db():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("students-db.html", students=students)

# Thêm sinh viên
@app.post("/students-db/add")
def add_student():
    student_id = request.form["student_id"].strip()
    fullname = request.form["fullname"].strip()
    dob = request.form["dob"].strip()
    major = request.form["major"].strip()

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (student_id, fullname, dob, major) VALUES (%s,%s,%s,%s)",
        (student_id, fullname, dob, major)
    )
    conn.commit()
    cursor.close()
    conn.close()

    # Trả về lại HTML cùng danh sách mới
    return students_db()

# Sửa sinh viên
@app.post("/students-db/edit/<int:id>")
def edit_student(id):
    student_id = request.form["student_id"].strip()
    fullname = request.form["fullname"].strip()
    dob = request.form["dob"].strip()
    major = request.form["major"].strip()

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET student_id=%s, fullname=%s, dob=%s, major=%s WHERE id=%s",
        (student_id, fullname, dob, major, id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return students_db()

# Xóa sinh viên
@app.post("/students-db/delete/<int:id>")
def delete_student(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return students_db()
    




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
