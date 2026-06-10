from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# ─── Data ─────────────────────────────────────────────────────────────────────

DATA_FILE = "SampleData.txt"
ADMIN_PASSWORD = "Nate_Diaz"
MAX_STUDENTS = 100

students = []  # list of dicts: {roll, name, section, marks:[5], grade}

# ─── Core logic ───────────────────────────────────────────────────────────────

def calculate_grade(marks):
    s = (0.4 * marks[0] + 0.3 * marks[1] +
         0.1 * marks[2] + 0.1 * marks[3] + 0.1 * marks[4])
    if s >= 90: return 'A'
    if s >= 80: return 'B'
    if s >= 60: return 'C'
    if s >= 40: return 'D'
    return 'F'

def load_from_file():
    global students
    students = []
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, 'r') as f:
        lines = f.read().split()
    if not lines:
        return
    idx = 0
    count = int(lines[idx]); idx += 1
    for _ in range(min(count, MAX_STUDENTS)):
        if idx + 8 >= len(lines):
            break
        roll    = int(lines[idx]);   idx += 1
        name    = lines[idx];        idx += 1
        section = lines[idx];        idx += 1
        marks   = [float(lines[idx+i]) for i in range(5)]; idx += 5
        grade   = lines[idx];        idx += 1
        students.append({
            'roll': roll, 'name': name, 'section': section,
            'marks': marks, 'grade': grade
        })

def save_to_file():
    with open(DATA_FILE, 'w') as f:
        f.write(f"{len(students)}\n")
        for s in students:
            f.write(f"{s['roll']} {s['name']} {s['section']} "
                    f"{s['marks'][0]} {s['marks'][1]} {s['marks'][2]} "
                    f"{s['marks'][3]} {s['marks'][4]} {s['grade']}\n")

# Load data on startup
load_from_file()

# ─── Serve frontend ───────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ─── Auth ─────────────────────────────────────────────────────────────────────

@app.route('/login/admin', methods=['POST'])
def admin_login():
    data = request.get_json()
    if not data or data.get('password') != ADMIN_PASSWORD:
        return jsonify(ok=False, error="Incorrect password")
    return jsonify(ok=True)

@app.route('/login/student', methods=['POST'])
def student_login():
    data = request.get_json()
    if not data or 'roll' not in data:
        return jsonify(ok=False, error="Missing roll number")
    roll = int(data['roll'])
    s = next((x for x in students if x['roll'] == roll), None)
    if not s:
        return jsonify(ok=False, error="Student not found")
    return jsonify(ok=True, data=s)

# ─── Read ─────────────────────────────────────────────────────────────────────

@app.route('/students', methods=['GET'])
def get_all_students():
    return jsonify(ok=True, data=students)

@app.route('/students/<int:roll>', methods=['GET'])
def get_student_by_roll(roll):
    s = next((x for x in students if x['roll'] == roll), None)
    if not s:
        return jsonify(ok=False, error="Student not found")
    return jsonify(ok=True, data=s)

@app.route('/students/section/<sec>', methods=['GET'])
def get_students_by_section(sec):
    result = [x for x in students if x['section'] == sec]
    return jsonify(ok=True, data=result)

@app.route('/students/grade/<grade>', methods=['GET'])
def get_students_by_grade(grade):
    result = [x for x in students if x['grade'] == grade]
    return jsonify(ok=True, data=result)

@app.route('/stats/section/<sec>', methods=['GET'])
def get_section_stats(sec):
    sec_students = [x for x in students if x['section'] == sec]
    if not sec_students:
        return jsonify(ok=False, error="No students in that section")

    total = len(sec_students)
    grade_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for s in sec_students:
        if s['grade'] in grade_count:
            grade_count[s['grade']] += 1

    subject_names = ['ENA', 'CP', 'Ideology', 'Quran', 'Islamiat']
    subjects = []
    for i, name in enumerate(subject_names):
        vals = [s['marks'][i] for s in sec_students]
        subjects.append({
            'name': name,
            'avg':  round(sum(vals) / total, 2),
            'high': max(vals),
            'low':  min(vals)
        })

    return jsonify(ok=True, data={
        'total':    total,
        'grades':   grade_count,
        'subjects': subjects
    })

# ─── Write ────────────────────────────────────────────────────────────────────

@app.route('/students', methods=['POST'])
def add_student():
    if len(students) >= MAX_STUDENTS:
        return jsonify(ok=False, error="Maximum capacity reached")

    data = request.get_json()
    if not data:
        return jsonify(ok=False, error="Missing data")

    roll    = data.get('roll')
    name    = data.get('name', '').strip()
    section = data.get('section', '')
    marks   = data.get('marks', [])

    if not roll or not (100000 <= int(roll) <= 999999):
        return jsonify(ok=False, error="Roll must be 6 digits")
    if not name:
        return jsonify(ok=False, error="Name is required")
    if section not in ('A', 'B'):
        return jsonify(ok=False, error="Section must be A or B")
    if len(marks) != 5 or not all(0 <= m <= 100 for m in marks):
        return jsonify(ok=False, error="Marks must be 5 values between 0-100")
    if any(s['roll'] == int(roll) for s in students):
        return jsonify(ok=False, error="Roll number already exists")

    new_student = {
        'roll':    int(roll),
        'name':    name,
        'section': section,
        'marks':   [float(m) for m in marks],
        'grade':   calculate_grade(marks)
    }
    students.append(new_student)
    save_to_file()
    return jsonify(ok=True, data=new_student)

@app.route('/students/<int:roll>', methods=['PUT'])
def update_student(roll):
    s = next((x for x in students if x['roll'] == roll), None)
    if not s:
        return jsonify(ok=False, error="Student not found")

    data = request.get_json()
    if not data:
        return jsonify(ok=False, error="Missing data")

    if 'name' in data and data['name'].strip():
        s['name'] = data['name'].strip()
    if 'section' in data and data['section'] in ('A', 'B'):
        s['section'] = data['section']
    if 'marks' in data:
        marks = data['marks']
        if len(marks) != 5 or not all(0 <= m <= 100 for m in marks):
            return jsonify(ok=False, error="Marks must be 5 values between 0-100")
        s['marks'] = [float(m) for m in marks]
        s['grade'] = calculate_grade(s['marks'])

    save_to_file()
    return jsonify(ok=True, data=s)

@app.route('/students/<int:roll>', methods=['DELETE'])
def delete_student(roll):
    global students
    original_count = len(students)
    students = [x for x in students if x['roll'] != roll]
    if len(students) == original_count:
        return jsonify(ok=False, error="Student not found")
    save_to_file()
    return jsonify(ok=True)

# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
