from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('songs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            embed_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('songs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM songs')
    songs = c.fetchall()
    conn.close()
    return render_template('index.html', songs=songs)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        embed_url = request.form['embed_url']

        conn = sqlite3.connect('songs.db')
        c = conn.cursor()
        c.execute('INSERT INTO songs (title, artist, embed_url) VALUES (?, ?, ?)',
                  (title, artist, embed_url))
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('post.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
    @app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # You can print it or save it to DB / send email
        print(f"New message from {name} ({email}): {message}")
        return "Thank you for contacting us! 🎉"

    return render_template('contact.html')

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store quiz answers temporarily
quiz_submissions = []

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    answers = {
        "q1": request.form["q1"],
        "q2": request.form["q2"],
        "q3": request.form["q3"],
        "q4": request.form["q4"],
        "q5": request.form["q5"]
    }
    quiz_submissions.append(answers)
    return "Your answers have been submitted! ✅"

@app.route("/admin/quiz-review")
def review_quiz():
    return render_template("quiz-review.html", submissions=quiz_submissions)

if __name__ == "__main__":
    app.run(debug=True)
