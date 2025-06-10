from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

conn_params = {
    "host": "dpg-d142ho8gjchc73fn7sr0-a.oregon-postgres.render.com",  # if DB is on this PC, otherwise put DB server IP
    "database": "mydb_ldig",
    "user": "tanvir",
    "password": "JgQGsLVOjXIDMyVm4zNuiiTjqgt50sJj",
    "port": 5432
}

def get_db_connection():
    return psycopg2.connect(**conn_params, cursor_factory=RealDictCursor)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def get_students():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, email FROM students ORDER BY id DESC")
        students = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "students": students})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')

    if not name or not age or not email:
        return jsonify({"status": "error", "message": "Please provide name, age, and email"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, age, email) VALUES (%s, %s, %s) RETURNING id",
            (name, age, email)
        )
        new_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "id": new_id, "message": "Student added successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Replace host='0.0.0.0' to allow access from other devices in the network
    app.run(host='0.0.0.0', port=5000, debug=True)
