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
