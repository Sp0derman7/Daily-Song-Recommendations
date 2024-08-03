import sqlite3
from datetime import datetime, timedelta
import random

DATABASE = 'Songs.db'


def create_table():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("""CREATE TABLE Songs (
                        Title TEXT,
                        Artist TEXT,
                        Time TEXT);""")
        print("Opened and created database successfully")

    except sqlite3.Error:
        print('Error in creating database')

    finally:
        if conn:
            conn.close()
            print("Connection closed")


def shuffle_songs():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # Retrieve all Date values from the Songs table
        c.execute("SELECT ID FROM Songs;")
        ids = [row[0] for row in c.fetchall()]

        # Shuffle the Date values
        random.shuffle(ids)

        # Retrieve all rows from the Songs table
        c.execute("SELECT * FROM Songs;")
        rows = c.fetchall()

        # Update the Songs table with the shuffled Date values
        for i, row in enumerate(rows):
            c.execute("UPDATE Songs SET ID=? WHERE Title=? AND Artist=? AND Time=? AND Date=?;",
                      (ids[i], row[0], row[1], row[2], row[3]))

        conn.commit()
        print("Song dates shuffled successfully")

    except sqlite3.Error as error:
        print("Error: ", error)

    finally:
        if conn:
            conn.close()


def add_song(title, artist, time):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(f"INSERT INTO Songs VALUES ('{title}', '{artist}', '{time}', 'Null', 'Null');")
        conn.commit()
        print("Record added successfully")

    except sqlite3.Error:
        print('Error in adding record')

    finally:
        if conn:
            conn.close()
            print("Connection closed")


def add_column(title, column_type):
    conn = None
    if all(isinstance(var, str) for var in (title, column_type)):
        try:
            column_type.upper()
            conn = sqlite3.connect("Songs.db")
            c = conn.cursor()
            c.execute(f"ALTER TABLE Songs ADD COLUMN {title} {column_type};")
            conn.commit()
            print(f"Column '{title}' added successfully")

        except sqlite3.Error as error:
            print("Error: ", error)

        finally:
            if conn:
                conn.close()

    else:
        print("Given title or type is not a string")


def remove_column(column_name):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # Get the existing columns except the one to be removed
        c.execute(f"PRAGMA table_info(Songs);")
        columns = [info[1] for info in c.fetchall() if info[1] != column_name]

        new_table = f"Songs_new"

        columns_str = ", ".join(columns)
        c.executescript(f"""CREATE TABLE {new_table} AS SELECT {columns_str} FROM Songs;
                  DROP TABLE Songs;
                  ALTER TABLE {new_table} RENAME TO Songs;""")

        conn.commit()
        print(f"Column '{column_name}' removed successfully from the database")

    except sqlite3.Error as error:
        print('Error:', error)

    finally:
        if conn:
            conn.close()
            print("Connection closed")


def set_date(date):
    conn = None
    try:
        conn = sqlite3.connect("Songs.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM Songs;")
        count = c.fetchone()[0]

        date = datetime.strptime(date, "%Y-%m-%d")

        for song in range(count):
            date_song_release = (date + timedelta(days=song)).strftime("%Y-%m-%d")
            c.execute("UPDATE Songs SET Date=? WHERE ID=?", (date_song_release, song + 1))
        conn.commit()
        print("Dates updated successfully")

    except sqlite3.Error as error:
        print("Error: ", error)

    finally:
        if conn:
            conn.close()


def get_song(title):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(f"SELECT * FROM Songs WHERE Title = '{title}';")
        rows = c.fetchall()
        for row in rows:
            print(row)

    except sqlite3.Error:
        print('Error in getting record')

    finally:
        if conn:
            conn.close()
            print("Connection closed")


def change_cell(change, column, row):
    print("cell")
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(f"""
        UPDATE Songs
        SET {column} = {change}
        WHERE ID = {row}
        """)
        print("changes made to cell")
    except sqlite3.Error as error:
        print("Error occurred while changing cell: ", error)

    finally:
        conn.close()


if __name__ == "__main__":
    get_song("Nathalie - Remasterisé en 2011")
