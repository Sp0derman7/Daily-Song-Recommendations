import sqlite3
from flask import Flask, render_template
from datetime import datetime
from os import path
import pytz

ROOT = path.dirname(path.realpath(__file__))

DATABASE = r"C:\Users\20234795\OneDrive\Daily-Song-Recommendations\Songs.db"

app = Flask(__name__, template_folder='html')


def song_now(current_date, current_time):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute("""SELECT Title, Artist, Time
                     FROM Songs
                     WHERE Date <= ? AND Time <= ?
                     ORDER BY Date DESC, Time DESC LIMIT 1;""", (current_date, current_time))
        row = c.fetchone()

        if not row:
            c.execute("""SELECT Title, Artist, Time
                         FROM Songs
                         WHERE Date < ?
                         ORDER BY Date DESC, Time DESC LIMIT 1;""", (current_date,))
            row = c.fetchone()

        return row if row else (None, None, None)
    except sqlite3.Error as error:
        print('Error in getting record:', error)
        return None, None, None
    finally:
        if conn:
            conn.close()


def time_till_next_song(current_date, current_time):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute("""SELECT Date, Time
                     FROM Songs
                     WHERE (Date = ? AND Time > ?) OR (Date > ?)
                     ORDER BY Date, Time LIMIT 1;""", (current_date, current_time, current_date))
        next_song = c.fetchone()

        if not next_song:
            c.execute("""SELECT Date, Time
                         FROM Songs
                         WHERE (Date = ? AND Time > ?) OR (Date > ?)
                         ORDER BY Date, Time LIMIT 1;""", (current_date, current_time, current_date))
            next_song = c.fetchone()

        if next_song:

            next_song_date_time = datetime.strptime(f"{next_song[0]} {next_song[1]}", "%Y-%m-%d %H:%M")
            current_date_time = datetime.strptime(f"{current_date} {current_time}", "%Y-%m-%d %H:%M")
            time_difference = next_song_date_time - current_date_time
            total_minutes = time_difference.total_seconds() / 60
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)

            return hours, minutes
        else:
            return None, None

    except sqlite3.Error as error:
        print('Error in getting record:', error)
        return None, None
    finally:
        if conn:
            conn.close()


def get_past_songs(current_date, current_time):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute("""SELECT Title, Artist, Date
                     FROM Songs
                     WHERE Date < ? OR (Date = ? AND Time < ?)
                     ORDER BY Date DESC, Time DESC;""", (current_date, current_date, current_time))
        rows = c.fetchall()
        return rows
    except sqlite3.Error as error:
        print('Error in getting records:', error)
        return []
    finally:
        if conn:
            conn.close()


@app.route("/")
def index():
    current_date = datetime.now(pytz.timezone('Europe/Amsterdam')).strftime("%Y-%m-%d")
    current_time = datetime.now(pytz.timezone('Europe/Amsterdam')).strftime("%H:%M")
    song_title, artist_name, time = song_now(current_date, current_time)
    hours, minutes = time_till_next_song(current_date, current_time)
    return render_template('index.html',
                           song_title=song_title,
                           artist_name=artist_name,
                           hour=hours,
                           min=minutes)


@app.route("/about")
def about():
    return render_template('About_this_site.html')


@app.route("/history")
def history():
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")
    past_songs = get_past_songs(current_date, current_time)
    return render_template('History.html', past_songs=past_songs)


if __name__ == "__main__":
    app.run(debug=True)
