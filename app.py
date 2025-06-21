from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecret"  # Change this for security

DATABASE = 'quiz.db'

CORRECT_ANSWERS = {
    "q1": "Sri Jayawardenepura Kotte",
    "q2": "Faizy",
    "q3": "Artificial Intelligence",
    "q4": "Faded",  # or accept many
    "q5": "Blue"
}

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB
def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            q1 TEXT, q2 TEXT, q3 TEXT, q4 TEXT, q5 TEXT,
            correct_q1 INTEGER, correct_q2 INTEGER,
            correct_q3 INTEGER, correct_q4 INTEGER, correct_q5 INTEGER
        )''')

@app.route('/')
def home():
    return render_template("quiz.html")

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    answers = {
        "q1": request.form.get("q1").strip(),
        "q2": request.form.get("q2").strip(),
        "q3": request.form.get("q3").strip(),
        "q4": request.form.get("q4").strip(),
        "q5": request.form.get("q5").strip()
    }

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    results = {}
    for key, user_answer in answers.items():
        correct = CORRECT_ANSWERS[key].lower() in user_answer.lower()
        results[f"correct_{key}"] = int(correct)

    with get_db() as db:
        db.execute('''INSERT INTO submissions 
            (timestamp, q1, q2, q3, q4, q5, correct_q1, correct_q2, correct_q3, correct_q4, correct_q5)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (timestamp, answers["q1"], answers["q2"], answers["q3"], answers["q4"], answers["q5"],
             results["correct_q1"], results["correct_q2"], results["correct_q3"], results["correct_q4"], results["correct_q5"])
        )
    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return "<h2 style='color: white; background:#0f172a; text-align:center; padding:50px;'>Thanks for submitting your answers!</h2>"

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'rws123':
            session['admin'] = True
            return redirect(url_for('quiz_review'))
        else:
            return "Invalid credentials"
    return render_template("login.html")

@app.route('/quiz-review')
def quiz_review():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    with get_db() as db:
        rows = db.execute("SELECT * FROM submissions ORDER BY timestamp DESC").fetchall()
    return render_template("quiz-review.html", submissions=rows)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
