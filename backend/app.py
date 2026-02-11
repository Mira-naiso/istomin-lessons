import os
import psycopg2
import redis
from flask import Flask, request, jsonify, redirect, url_for, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

PG_HOST = os.getenv("POSTGRES_HOST")
PG_PORT = os.getenv("POSTGRES_PORT", "5432")
PG_DB = os.getenv("POSTGRES_DB")
PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

def get_pg_conn():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

HTML_REGISTER = """
<h2>Регистрация</h2>
<form method="post" action="/register">
  Email: <input type="email" name="email" required><br>
  Name: <input type="text" name="name" required><br>
  <button type="submit">Зарегистрироваться</button>
</form>
<a href="/login-page">Войти</a>
"""

HTML_LOGIN = """
<h2>Вход</h2>
<form method="post" action="/login">
  Email: <input type="email" name="email" required><br>
  Name: <input type="text" name="name" required><br>
  <button type="submit">Войти</button>
</form>
<a href="/">Регистрация</a>
"""

@app.route("/")
def index():
    return render_template_string(HTML_REGISTER)

@app.route("/login-page")
def login_page():
    return render_template_string(HTML_LOGIN)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    name = request.form.get("name")

    conn = get_pg_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE,
            name TEXT
        )
    """)
    cur.execute("INSERT INTO users (email, name) VALUES (%s, %s)", (email, name))
    conn.commit()
    cur.close()
    conn.close()

    return "<p>Успешно зарегистрирован!</p><a href='/login-page'>Войти</a>"

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    name = request.form.get("name")

    conn = get_pg_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM users WHERE email=%s", (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row or row[0] != name:
        return "<p>Неверные данные</p><a href='/login-page'>Попробовать снова</a>"

    r.set(f"session:{email}", "logged_in", ex=3600)
    return "<p>Успешный вход!</p><a href='/'>На главную</a>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
