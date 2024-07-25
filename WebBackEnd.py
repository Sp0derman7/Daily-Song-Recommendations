import sqlite3
from flask import Flask, render_template

app = Flask(__name__, template_folder='html')


def get_most_recent_song_before_date(date):
    conn = None
    try:
        conn = sqlite3.connect('Songs.db')
        c = conn.cursor()
        c.execute("SELECT Title, Artist FROM Songs WHERE Date < ? ORDER BY Date DESC LIMIT 1;", (date,))
        row = c.fetchone()
        return row if row else (None, None)
    except sqlite3.Error as error:
        print('Error in getting record:', error)
        return None, None
    finally:
        if conn:
            conn.close()


@app.route("/")
def index():
    song_title, artist_name = get_most_recent_song_before_date('2024-07-27')
    print(song_title, artist_name)
    return render_template('index.html', song_title=song_title, artist_name=artist_name)


if __name__ == "__main__":
    app.run(debug=True)
