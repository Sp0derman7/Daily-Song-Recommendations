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
        conn = sqlite3.connect('Songs.db')
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


def set_date():
    print("date")


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
    add_column("Date", "TEXT")
