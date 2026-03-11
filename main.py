import mysql.connector
from mysql.connector import Error

HOST = "cssql.seattleu.edu"
PORT = 3306
USER = "ll_qpham5"
PASSWORD = "HYxOW8OWEY3o52/4"
DATABASE = "ll_qpham5"

def main():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            connection_timeout=10
        )
        print("Connected:", conn.is_connected())

        cur = conn.cursor()
        cur.execute("select database(), user(), version();")
        print("Info:", cur.fetchone())

        cur.execute("show tables;")
        print("Tables:")
        for (t,) in cur.fetchall():
            print("-", t)

        cur.close()
        conn.close()
        print("Closed connection.")

    except Error as e:
        print("MySQL error:", e)

if __name__ == "__main__":
    main()