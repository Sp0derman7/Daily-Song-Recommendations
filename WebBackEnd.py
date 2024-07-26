import sqlite3
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__, template_folder='html')


def song_now(current_date, current_time):
    conn = None
    try:
        conn = sqlite3.connect('Songs.db')
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
                          ORDER BY Date DESC, Time DESC LIMIT 1;""", current_date)
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
        conn = sqlite3.connect('Songs.db')
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
            print(next_song_date_time)
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


@app.route("/")
def index():
    current_date = "2024-07-27"
    current_time = "14:00"
    song_title, artist_name, time = song_now(current_date, current_time)
    hours, minutes = time_till_next_song(current_date, current_time)
    return render_template('index.html',
                           song_title=song_title,
                           artist_name=artist_name,
                           hour=hours,
                           min=minutes)


if __name__ == "__main__":
    app.run(debug=True)
