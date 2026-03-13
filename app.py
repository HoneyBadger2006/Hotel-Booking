from flask import Flask, request, redirect, session, render_template_string, url_for
import mysql.connector as mc
from mysql.connector import Error
from datetime import date

app = Flask(__name__)
app.secret_key = "change_this_demo_secret"

DB = dict(
    host="cssql.seattleu.edu",
    port=3306,
    user="ll_qpham5",
    password="HYxQW8OWEY3o52/4",
    database="ll_qpham5",
    connection_timeout=10,
    use_pure=True
)

def get_conn():
    return mc.connect(**DB)

def current_user_id():
    return session.get("user_id")

BASE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Hotel Booking Demo</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
  .hero { background: #0b5ed7; color: white; border-radius: 18px; padding: 28px; }
  .card-soft { border: 1px solid #e9ecef; border-radius: 16px; }
  .muted { color:#6c757d; }
  .pill { font-size: 12px; }
  .btn-book { border-radius: 999px; padding-left: 16px; padding-right: 16px; }

  /* effects */
  .lift { transition: transform .18s ease, box-shadow .18s ease; }
  .lift:hover { transform: translateY(-4px); box-shadow: 0 12px 28px rgba(0,0,0,.12) !important; }
  .fade-in { animation: fadeIn .45s ease both; }
  @keyframes fadeIn { from {opacity:0; transform: translateY(8px);} to {opacity:1; transform:none;} }

  /* ad */
  .ad-card img { width:100%; height: 220px; object-fit: cover; border-radius: 16px; }
  .ad-badge { position:absolute; top:12px; left:12px; }
</style>
</head>
<body class="bg-light">
<nav class="navbar navbar-expand-lg bg-white border-bottom">
  <div class="container">
    <a class="navbar-brand fw-bold" href="/">Booking Demo</a>
    <div class="d-flex gap-2 align-items-center">
      <a class="btn btn-outline-primary btn-sm" href="/search">Search</a>
      <a class="btn btn-outline-secondary btn-sm" href="/my-bookings">My bookings</a>
      {% if user_id %}
        <span class="small muted">user_id={{user_id}}</span>
        <a class="btn btn-danger btn-sm" href="/logout">Logout</a>
      {% else %}
        <a class="btn btn-primary btn-sm" href="/login">Login</a>
        <a class="btn btn-outline-primary btn-sm" href="/register">Register</a>
      {% endif %}
    </div>
  </div>
</nav>

<div class="container my-4">
  {{ body|safe }}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

HOME_BODY = """
<div class="hero mb-4 fade-in">
  <h2 class="mb-1">Find your next stay</h2>
  <p class="mb-0">Demo UI inspired by Booking.com. Login, search, and book a room.</p>
</div>

<div class="row g-3 mb-2">
  <div class="col-12 col-lg-8">
    <div class="card card-soft shadow-sm lift fade-in">
      <div class="card-body">
        <h5 class="mb-1">Deal of the day</h5>
        <div class="muted">Limited-time promo for demo purposes</div>
        <div class="mt-3 d-flex gap-2">
          <a class="btn btn-dark btn-book" href="/search">Search deals</a>
          <a class="btn btn-outline-primary btn-book" href="/my-bookings">My bookings</a>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="d-flex justify-content-between align-items-center mb-3 mt-3">
  <h4 class="mb-0">Hotels</h4>
  <a class="btn btn-primary btn-sm btn-book" href="/search">Search rooms</a>
</div>

<div class="row g-3">
  {% for h in hotels %}
  <div class="col-12 col-md-6 col-lg-4">
    <div class="card card-soft shadow-sm h-100 lift fade-in">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-start">
          <div>
            <h5 class="card-title mb-1">{{h[1]}}</h5>
            <div class="muted small">{{h[2]}}{% if h[3] %}, {{h[3]}}{% endif %} · {{h[4]}}</div>
          </div>
          <span class="badge text-bg-light pill">hotel_id {{h[0]}}</span>
        </div>

        <div class="mt-3 d-flex gap-2">
          <a class="btn btn-outline-primary btn-sm btn-book" href="/hotel/{{h[0]}}">View rooms</a>
          <a class="btn btn-primary btn-sm btn-book" href="/search?city={{h[2]}}">Search city</a>
        </div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>
"""

REGISTER_BODY = """
<div class="row justify-content-center">
  <div class="col-12 col-md-7">
    <div class="card card-soft shadow-sm">
      <div class="card-body">
        <h4 class="mb-3">Create account</h4>
        <form method="post">
          <div class="row g-3">
            <div class="col-12">
              <label class="form-label">Email</label>
              <input class="form-control" name="email" required>
            </div>
            <div class="col-12">
              <label class="form-label">Password</label>
              <input class="form-control" name="password" type="password" required>
              <div class="form-text">Demo only: stored as plain text in password_hash.</div>
            </div>
            <div class="col-12 col-md-8">
              <label class="form-label">Full name</label>
              <input class="form-control" name="full_name" required>
            </div>
            <div class="col-12 col-md-4">
              <label class="form-label">Phone</label>
              <input class="form-control" name="phone">
            </div>
          </div>
          <button class="btn btn-primary w-100 mt-3" type="submit">Register</button>
        </form>

        {% if error %}
          <div class="alert alert-danger mt-3 mb-0">{{error}}</div>
        {% endif %}
      </div>
    </div>
  </div>
</div>
"""

LOGIN_BODY = """
<div class="row justify-content-center">
  <div class="col-12 col-md-6">
    <div class="card card-soft shadow-sm">
      <div class="card-body">
        <h4 class="mb-3">Login</h4>
        <form method="post">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input class="form-control" name="email" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input class="form-control" name="password" type="password" required>
          </div>
          <button class="btn btn-primary w-100" type="submit">Login</button>
        </form>

        {% if error %}
          <div class="alert alert-danger mt-3 mb-0">{{error}}</div>
        {% endif %}
      </div>
    </div>
  </div>
</div>
"""

HOTEL_BODY = """
<div class="mb-3">
  <h3 class="mb-1">{{hotel[1]}}</h3>
  <div class="muted">{{hotel[2]}}{% if hotel[3] %}, {{hotel[3]}}{% endif %} · {{hotel[4]}} · hotel_id {{hotel[0]}}</div>
</div>

<div class="row g-3">
  {% for r in rooms %}
  <div class="col-12">
    <div class="card card-soft shadow-sm">
      <div class="card-body d-flex flex-column flex-md-row justify-content-between gap-3">
        <div>
          <div class="d-flex gap-2 align-items-center mb-1">
            <span class="badge text-bg-light">Room {{r[0]}}</span>
            <span class="badge text-bg-primary">{{r[1]}}</span>
            <span class="badge text-bg-secondary">Capacity {{r[2]}}</span>
            <span class="badge text-bg-success">${{r[3]}}/night</span>
          </div>
          <div class="muted">{{r[4]}}</div>
        </div>
        <div class="text-end">
          <a class="btn btn-primary btn-book"
             href="/book?hotel_id={{hotel[0]}}&room_no={{r[0]}}">
             Book now
          </a>
        </div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>
"""

SEARCH_BODY = """
<div class="hero mb-4">
  <h3 class="mb-2">Search</h3>
  <form class="row g-2" method="get">
    <div class="col-12 col-md-5">
      <input class="form-control" name="city" value="{{city}}" placeholder="City (e.g., Seattle)">
    </div>
    <div class="col-6 col-md-3">
      <input class="form-control" name="check_in" type="date" value="{{check_in}}">
    </div>
    <div class="col-6 col-md-3">
      <input class="form-control" name="check_out" type="date" value="{{check_out}}">
    </div>
    <div class="col-12 col-md-1 d-grid">
      <button class="btn btn-dark" type="submit">Go</button>
    </div>
  </form>
</div>

{% if error %}
  <div class="alert alert-danger">{{error}}</div>
{% endif %}

{% if results is not none %}
  <div class="d-flex justify-content-between align-items-center mb-2">
    <h5 class="mb-0">Results</h5>
    <div class="muted small">{{results|length}} matches</div>
  </div>

  <div class="card card-soft shadow-sm">
    <div class="table-responsive">
      <table class="table table-hover mb-0 align-middle">
        <thead class="table-light">
          <tr>
            <th>Hotel</th><th>City</th><th>Room</th><th>Type</th><th>Capacity</th><th>Price/night</th><th></th>
          </tr>
        </thead>
        <tbody>
          {% for x in results %}
          <tr>
            <td>
              <div class="fw-semibold">{{x[0]}}</div>
              <div class="muted small">hotel_id {{x[1]}}</div>
            </td>
            <td>{{x[2]}}</td>
            <td>{{x[3]}}</td>
            <td>{{x[4]}}</td>
            <td>{{x[5]}}</td>
            <td>${{x[6]}}</td>
            <td class="text-end">
              <a class="btn btn-primary btn-sm btn-book"
                 href="/book?hotel_id={{x[1]}}&room_no={{x[3]}}&check_in={{check_in}}&check_out={{check_out}}">
                Book
              </a>
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
{% endif %}
"""

BOOK_BODY = """
<div class="card card-soft shadow-sm">
  <div class="card-body">
    <h4 class="mb-1">Book room</h4>
    <div class="muted mb-3">Hotel ID {{hotel_id}} · Room {{room_no}}</div>

    {% if not user_id %}
      <div class="alert alert-warning mb-3">You must login before booking.</div>
      <a class="btn btn-primary" href="/login">Go to login</a>
    {% else %}
      <form method="post" class="row g-3">
        <input type="hidden" name="hotel_id" value="{{hotel_id}}">
        <input type="hidden" name="room_no" value="{{room_no}}">

        <div class="col-12 col-md-5">
          <label class="form-label">Check-in</label>
          <input class="form-control" name="check_in" type="date" value="{{check_in}}" required>
        </div>
        <div class="col-12 col-md-5">
          <label class="form-label">Check-out</label>
          <input class="form-control" name="check_out" type="date" value="{{check_out}}" required>
        </div>
        <div class="col-12 col-md-2 d-grid align-items-end">
          <button class="btn btn-primary btn-book" type="submit">Confirm</button>
        </div>
      </form>
    {% endif %}

    {% if error %}
      <div class="alert alert-danger mt-3 mb-0">{{error}}</div>
    {% endif %}
    {% if ok %}
      <div class="alert alert-success mt-3 mb-0">{{ok}}</div>
    {% endif %}
  </div>
</div>
"""

MYBOOK_BODY = """
<h4 class="mb-3">My bookings</h4>

{% if not user_id %}
  <div class="alert alert-warning">Please login to view your bookings.</div>
{% else %}
  <div class="card card-soft shadow-sm">
    <div class="table-responsive">
      <table class="table table-hover mb-0 align-middle">
        <thead class="table-light">
          <tr>
            <th>booking_id</th><th>hotel</th><th>room</th><th>check-in</th><th>check-out</th><th>status</th><th>created_at</th>
          </tr>
        </thead>
        <tbody>
          {% for b in bookings %}
          <tr>
            <td class="fw-semibold">{{b[0]}}</td>
            <td>{{b[1]}} <span class="muted small">(id {{b[2]}})</span></td>
            <td>{{b[3]}}</td>
            <td>{{b[4]}}</td>
            <td>{{b[5]}}</td>
            <td><span class="badge text-bg-light">{{b[6]}}</span></td>
            <td class="muted small">{{b[7]}}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
{% endif %}
{% if msg %}
  <div class="alert alert-info">{{msg}}</div>
{% endif %}
<form method="post" action="/booking/{{b[0]}}/status" style="display:inline;">
  <input type="hidden" name="status" value="Cancelled">
  <button class="btn btn-outline-danger btn-sm" type="submit">Cancel</button>
</form>

<form method="post" action="/booking/{{b[0]}}/status" style="display:inline;">
  <input type="hidden" name="status" value="Refunded">
  <button class="btn btn-outline-warning btn-sm" type="submit">Refund</button>
</form>
"""

@app.route("/")
def home():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("select hotel_id, name, city, state, country from Hotel order by hotel_id;")
    hotels = cur.fetchall()
    cur.close()
    conn.close()
    return render_template_string(BASE, body=render_template_string(HOME_BODY, hotels=hotels), user_id=current_user_id())

@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":
        email = request.form["email"].strip()
        pw = request.form["password"]
        full_name = request.form["full_name"].strip()
        phone = request.form.get("phone", "").strip() or None

        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "insert into Guest (email, password_hash, full_name, phone) values (%s,%s,%s,%s)",
                (email, pw, full_name, phone)  # demo only: storing plain password in password_hash
            )
            conn.commit()
            user_id = cur.lastrowid
            cur.close()
            conn.close()
            session["user_id"] = user_id
            return redirect("/")
        except Error as e:
            error = str(e)

    return render_template_string(BASE, body=render_template_string(REGISTER_BODY, error=error), user_id=current_user_id())

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        email = request.form["email"].strip()
        pw = request.form["password"]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("select user_id, password_hash from Guest where email=%s", (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            error = "Email not found"
        else:
            user_id, stored = row
            if pw != stored:
                error = "Wrong password"
            else:
                session["user_id"] = user_id
                return redirect("/")

    return render_template_string(BASE, body=render_template_string(LOGIN_BODY, error=error), user_id=current_user_id())

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

@app.route("/hotel/<int:hotel_id>")
def hotel_page(hotel_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("select hotel_id, name, city, state, country from Hotel where hotel_id=%s", (hotel_id,))
    hotel = cur.fetchone()

    cur.execute("""
        select r.room_no, rt.name, rt.capacity, rt.price_per_night, r.description
        from Room r
        join Room_Type rt on rt.room_type_id = r.room_type_id
        where r.hotel_id=%s
        order by r.room_no;
    """, (hotel_id,))
    rooms = cur.fetchall()

    cur.close()
    conn.close()

    return render_template_string(BASE, body=render_template_string(HOTEL_BODY, hotel=hotel, rooms=rooms), user_id=current_user_id())

@app.route("/search")
def search():
    city = request.args.get("city", "").strip()
    check_in = request.args.get("check_in", "")
    check_out = request.args.get("check_out", "")
    results = None
    error = ""

    if city or check_in or check_out:
        if not (check_in and check_out):
            error = "Please enter both check-in and check-out."
        else:
            conn = get_conn()
            cur = conn.cursor()

            # show rooms in a city, and exclude rooms that have overlapping CONFIRMED bookings
            cur.execute("""
                select
                  h.name, h.hotel_id, h.city,
                  r.room_no,
                  rt.name as room_type,
                  rt.capacity,
                  rt.price_per_night
                from Hotel h
                join Room r on r.hotel_id = h.hotel_id
                join Room_Type rt on rt.room_type_id = r.room_type_id
                where (%s = '' or h.city like concat('%', %s, '%'))
                  and not exists (
                    select 1
                    from Booking b
                    where b.hotel_id = r.hotel_id
                      and b.room_no = r.room_no
                      and b.status = 'Confirmed'
                      and %s < b.check_out_date
                      and %s > b.check_in_date
                  )
                order by h.hotel_id, r.room_no;
            """, (city, city, check_in, check_out))

            results = cur.fetchall()
            cur.close()
            conn.close()

    return render_template_string(
        BASE,
        body=render_template_string(SEARCH_BODY, city=city, check_in=check_in, check_out=check_out, results=results, error=error),
        user_id=current_user_id()
    )

@app.route("/book", methods=["GET", "POST"])
def book():
    user_id = current_user_id()
    error = ""
    ok = ""

    if request.method == "GET":
        hotel_id = request.args.get("hotel_id", "")
        room_no = request.args.get("room_no", "")
        check_in = request.args.get("check_in", "")
        check_out = request.args.get("check_out", "")
        return render_template_string(
            BASE,
            body=render_template_string(BOOK_BODY, user_id=user_id, hotel_id=hotel_id, room_no=room_no,
                                        check_in=check_in, check_out=check_out, error=error, ok=ok),
            user_id=user_id
        )

    hotel_id = int(request.form["hotel_id"])
    room_no = int(request.form["room_no"])
    check_in = request.form["check_in"]
    check_out = request.form["check_out"]

    if not user_id:
        error = "Please login first."
    else:
        try:
            conn = get_conn()
            cur = conn.cursor()

            # quick conflict check (your trigger can also enforce this)
            cur.execute("""
                select 1
                from Booking b
                where b.hotel_id=%s and b.room_no=%s and b.status='Confirmed'
                  and %s < b.check_out_date and %s > b.check_in_date
                limit 1;
            """, (hotel_id, room_no, check_in, check_out))
            conflict = cur.fetchone()

            if conflict:
                error = "Conflict: room already booked for those dates."
            else:
                cur.execute("""
                    insert into Booking (user_id, room_no, hotel_id, check_in_date, check_out_date, status, created_at)
                    values (%s,%s,%s,%s,%s,'Confirmed', now());
                """, (user_id, room_no, hotel_id, check_in, check_out))
                conn.commit()
                ok = "Booking created!"

            cur.close()
            conn.close()

        except Error as e:
            error = str(e)

    return render_template_string(
        BASE,
        body=render_template_string(BOOK_BODY, user_id=user_id, hotel_id=hotel_id, room_no=room_no,
                                    check_in=check_in, check_out=check_out, error=error, ok=ok),
        user_id=user_id
    )

@app.route("/my-bookings")
def my_bookings():
    user_id = current_user_id()
    bookings = []
    if user_id:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            select b.booking_id, h.name, b.hotel_id, b.room_no, b.check_in_date, b.check_out_date, b.status, b.created_at
            from Booking b
            join Hotel h on h.hotel_id = b.hotel_id
            where b.user_id = %s
            order by b.booking_id desc;
        """, (user_id,))
        bookings = cur.fetchall()
        cur.close()
        conn.close()
        msg = request.args.get("msg", "")
    return render_template_string(BASE, body=render_template_string(MYBOOK_BODY, user_id=user_id, bookings=bookings), user_id=user_id)

@app.post("/booking/<int:booking_id>/status")
def update_booking_status(booking_id):
    if not current_user_id():
        return redirect("/login")

    new_status = request.form["status"]  # "Cancelled" or "Refunded"
    uid = current_user_id()

    conn = get_conn()
    cur = conn.cursor()

    # get current status (only for this user's booking)
    cur.execute(
        "select status from Booking where booking_id=%s and user_id=%s",
        (booking_id, uid)
    )
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return redirect("/my-bookings?msg=Booking+not+found")

    current_status = row[0]

    allowed = False
    if new_status == "Refunded" and current_status in ("Confirmed", "Completed"):
        allowed = True
    if new_status == "Cancelled" and current_status in ("Pending", "Confirmed"):
        allowed = True

    if not allowed:
        cur.close(); conn.close()
        return redirect("/my-bookings?msg=Not+allowed+from+" + str(current_status))

    cur.execute(
        "update Booking set status=%s where booking_id=%s and user_id=%s",
        (new_status, booking_id, uid)
    )
    conn.commit()

    cur.close()
    conn.close()
    return redirect("/my-bookings?msg=Updated")

if __name__ == "__main__":
    app.run(debug=True)