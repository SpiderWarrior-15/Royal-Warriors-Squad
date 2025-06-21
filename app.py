from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import json

app = Flask(__name__)

# File to store quiz submissions
DATA_FILE = "submissions.json"

# Load submissions if file exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        submissions = json.load(f)
else:
    submissions = []

@app.route('/')
def home():
    return render_template("quiz.html")

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    user_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "q1": request.form.get("q1"),
        "q2": request.form.get("q2"),
        "q3": request.form.get("q3"),
        "q4": request.form.get("q4"),
        "q5": request.form.get("q5")
    }

    # Save new submission
    submissions.append(user_data)

    with open(DATA_FILE, "w") as f:
        json.dump(submissions, f, indent=2)

    return redirect(url_for('review_quiz'))

@app.route('/quiz-review')
def review_quiz():
    return render_template("quiz-review.html", submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True)
