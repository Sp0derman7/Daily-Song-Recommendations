import sqlite3


def create_table():
    conn = None
    try:
        conn = sqlite3.connect('Songs.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE Songs (
                        Title TEXT,
                        Artist TEXT,
                        Time TEXT);""")
        print("Opened and created database successfully")

    except sqlite3.Error as error:
        print('Error in creating database')

    finally:
        if conn:
            conn.close()
            print("Connection closed")


def add_song(title, artist, time):
    conn = None
    try:
        conn = sqlite3.connect('Songs.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO Songs VALUES ('{title}', '{artist}', '{time}');")
        conn.commit()
        print("Record added successfully")

    except sqlite3.Error as error:
        print('Error in adding record')

    finally:
        if conn:
            conn.close()
            print("Connection closed")


def get_song(title):
    conn = None
    try:
        conn = sqlite3.connect('Songs.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM Songs WHERE Title = '{title}';")
        rows = c.fetchall()
        for row in rows:
            print(row)

    except sqlite3.Error as error:
        print('Error in getting record')

    finally:
        if conn:
            conn.close()
            print("Connection closed")


if __name__ == "__main__":
    print("main")
