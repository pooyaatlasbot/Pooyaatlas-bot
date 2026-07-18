import sqlite3
import os

DATABASE_NAME = "database/users.db"


def create_database():
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_code TEXT UNIQUE,

        full_name TEXT,
        phone TEXT,
        national_code TEXT,
        birth_date TEXT,
        city TEXT,
        education TEXT,
        course TEXT,

        has_flight_experience TEXT,

        photo TEXT,
        national_card TEXT,
        birth_certificate TEXT,
        education_file TEXT,
        medical_file TEXT,

        register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def add_student(
    tracking_code,
    full_name,
    phone,
    national_code,
    birth_date,
    city,
    education,
    course,
    has_flight_experience,
    photo="",
    national_card="",
    birth_certificate="",
    education_file="",
    medical_file=""
):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students(
        tracking_code,
        full_name,
        phone,
        national_code,
        birth_date,
        city,
        education,
        course,
        has_flight_experience,
        photo,
        national_card,
        birth_certificate,
        education_file,
        medical_file
    )
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        tracking_code,
        full_name,
        phone,
        national_code,
        birth_date,
        city,
        education,
        course,
        has_flight_experience,
        photo,
        national_card,
        birth_certificate,
        education_file,
        medical_file
    ))

    conn.commit()
    conn.close()


def get_student(tracking_code):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE tracking_code=?",
        (tracking_code,)
    )

    data = cursor.fetchone()

    conn.close()

    return data


def get_all_students():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM students
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data