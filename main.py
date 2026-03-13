# milestone3_main.py
import mysql.connector as mc
from mysql.connector import Error

HOST = "cssql.seattleu.edu"
PORT = 3306
USER = "ll_qpham5"
PASSWORD = "HYxQW8OWEY3o52/4"
DATABASE = "ll_qpham5"

def print_rows(title, cols, rows, limit=15):
    print("\n" + "=" * 80)
    print(title)
    print("-" * 80)
    print("columns:", cols)
    print("rows:", len(rows))
    for i, r in enumerate(rows[:limit], 1):
        print(i, r)
    if len(rows) > limit:
        print(f"... showing first {limit} rows")

def run_select(cur, title, sql, params=None):
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description] if cur.description else []
    print_rows(title, cols, rows)
    return rows

def run_write(cur, conn, title, sql, params=None):
    print("\n" + "=" * 80)
    print(title)
    print("-" * 80)
    cur.execute(sql, params or ())
    conn.commit()
    print("rows affected:", cur.rowcount)

def main():
    try:
        print("CONNECTING...")
        conn = mc.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            connection_timeout=10,
            use_pure=True
        )
        print("CONNECTED:", conn.is_connected())

        cur = conn.cursor()

        # proof of connection
        run_select(cur, "Connection Check", "select database() as db, user() as user, now() as now;")

        # ----------------------------
        # WRITE OPERATION (INSERT)
        # ----------------------------
        run_write(
            cur, conn,
            "WRITE: Insert a new review (demo)",
            """
            insert into Review (user_id, hotel_id, rating, title, body, created_at)
            values (%s, %s, %s, %s, %s, now());
            """,
            (1, 1, 9, "Milestone 3 test", "Inserted from Python Milestone 3 script")
        )

        # show the inserted row
        run_select(
            cur,
            "Verify INSERT (latest reviews by user 1 at hotel 1)",
            """
            select review_id, user_id, hotel_id, rating, title, created_at
            from Review
            where user_id = 1 and hotel_id = 1
            order by review_id desc
            limit 5;
            """

        )
        #Delete the inserted row to keep the database clean for the next run
        run_write(
            cur, conn,
            "CLEANUP: Delete the inserted review",
            """
            DELETE from Review
            where user_id = 1 and hotel_id = 1 and title = %s and body = %s;
            """,
            ("Milestone 3 test", "Inserted from Python Milestone 3 script")
        )

        # ----------------------------
        # FIVE QUERIES (paste your Milestone 2 Q4 queries here)
        # ----------------------------
        QUERIES = [
            ("Q1 (Milestone 2 #4 Query 1)", """
                select
                  b.booking_id,
                  g.full_name,
                  h.name as hotel_name,
                  b.hotel_id,
                  b.room_no,
                  b.check_in_date,
                  b.check_out_date,
                  b.status
                from Booking b
                join Guest g on b.user_id = g.user_id
                join Hotel h on b.hotel_id = h.hotel_id
                order by b.booking_id;
            """),

            ("Q2 (Milestone 2 #4 Query 2)", """
                select h.hotel_id, h.name, count(b.booking_id) as booking_count
                from Hotel h
                left join Booking b on b.hotel_id = h.hotel_id
                group by h.hotel_id, h.name
                order by booking_count desc;
            """),

            ("Q3 (Milestone 2 #4 Query 3)", """
                select g.user_id, g.full_name, avg(r.rating) as avg_rating
                from Guest g
                join Review r on r.user_id = g.user_id
                group by g.user_id, g.full_name
                order by avg_rating desc;
            """),

            ("Q4 (Milestone 2 #4 Query 4)", """
                select a.name, count(*) as times_used
                from Room_amenity ra
                join Amenity a on a.amenity_id = ra.amenity_id
                group by a.amenity_id, a.name
                order by times_used desc;
            """),

            ("Q5 (Milestone 2 #4 Query 5)", """
                select rt.name as room_type, count(*) as room_count
                from Room r
                join Room_Type rt on rt.room_type_id = r.room_type_id
                group by rt.room_type_id, rt.name
                order by room_count desc;
            """),
        ]

        for title, sql in QUERIES:
            run_select(cur, title, sql)

        cur.close()
        conn.close()
        print("\nDONE. Connection closed.")

    except Error as e:
        print("MySQL error:", e)

if __name__ == "__main__":
    main()
    