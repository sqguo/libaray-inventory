import mysql.connector

# environment variables
DATABASE_HOST3 = 'marmoset03.shoshin.uwaterloo.ca'
DATABASE_HOST4 = 'marmoset04.shoshin.uwaterloo.ca'
DATABASE_NAME = 'db356_sqguo'
DATABASE_USER = 'sqguo'
DATABASE_PASSWORD = 'db^iRL78UuhseLYzcz@6'

conn = None
cursor = None

# connect to the database
def connect_db():
    global conn
    global cursor
    conn = mysql.connector.connect(
        host=DATABASE_HOST3,
        database=DATABASE_NAME,
        user=DATABASE_USER,
        passwd=DATABASE_PASSWORD
    )
    cursor = conn.cursor()

# run a sql script
def load_script(path):
    with open(path, 'r') as f:
        try:
            for _ in cursor.execute(f.read(), multi=True): pass
            conn.commit()
            print("...loaded script:", path)
        except mysql.connector.Error as err:
            print("script went wrong: {}".format(err))

# insert rows of data
def load_data(sql, data, identifier=None, defer_commit=False):
    try:
        cursor.executemany(sql, data)
        if not defer_commit:
            conn.commit()
        return True
    except mysql.connector.Error as err:
        print("Insertion went wrong: {}".format(err))
        if identifier:
            f = open("./temp/log.txt", "a")
            f.write("{}\n".format(identifier))
            f.close()
    return False

# select some rows
def fetch_data(sql):
    cursor.execute(sql)
    return cursor

# clean up
def close_db():
    cursor.close()
    conn.close()