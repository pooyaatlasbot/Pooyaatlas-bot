import sqlite3
from pathlib import Path
from typing import Optional

from config import DATABASE_NAME


DATABASE_PATH = Path(DATABASE_NAME)


def get_connection() -> sqlite3.Connection:
    """
    ایجاد اتصال استاندارد به دیتابیس.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        str(DATABASE_PATH),
        timeout=30,
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    connection.execute(
        "PRAGMA busy_timeout = 30000"
    )

    return connection


def create_database() -> None:
    """
    ایجاد جدول‌های موردنیاز ربات.
    """

    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                tracking_code TEXT NOT NULL UNIQUE,

                telegram_id INTEGER,
                telegram_username TEXT,

                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                national_code TEXT NOT NULL,
                birth_date TEXT,
                city TEXT,
                education TEXT,
                course TEXT NOT NULL,

                has_flight_experience TEXT DEFAULT 'خیر',

                photo TEXT DEFAULT '',
                national_card TEXT DEFAULT '',
                birth_certificate TEXT DEFAULT '',
                education_file TEXT DEFAULT '',
                medical_file TEXT DEFAULT '',

                signed_contract TEXT DEFAULT '',
                contract_received INTEGER DEFAULT 0,

                register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_students_tracking_code
            ON students(tracking_code)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_students_phone
            ON students(phone)
            """
        )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_students_national_code
            ON students(national_code)
            """
        )


def add_student(
    tracking_code: str,
    full_name: str,
    phone: str,
    national_code: str,
    birth_date: str,
    city: str,
    education: str,
    course: str,
    has_flight_experience: str = "خیر",
    telegram_id: Optional[int] = None,
    telegram_username: str = "",
    photo: str = "",
    national_card: str = "",
    birth_certificate: str = "",
    education_file: str = "",
    medical_file: str = "",
) -> int:
    """
    ذخیره اطلاعات هنرجو و برگرداندن شناسه رکورد.
    """

    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO students (
                    tracking_code,
                    telegram_id,
                    telegram_username,
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
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    tracking_code,
                    telegram_id,
                    telegram_username,
                    full_name.strip(),
                    phone.strip(),
                    national_code.strip(),
                    birth_date.strip(),
                    city.strip(),
                    education.strip(),
                    course.strip(),
                    has_flight_experience,
                    photo,
                    national_card,
                    birth_certificate,
                    education_file,
                    medical_file,
                ),
            )

            return cursor.lastrowid

    except sqlite3.IntegrityError as exc:
        raise ValueError(
            "کد رهگیری تکراری است یا اطلاعات معتبر نیست."
        ) from exc


def get_student(
    tracking_code: str,
) -> Optional[dict]:
    """
    دریافت اطلاعات هنرجو با کد رهگیری.
    """

    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT *
            FROM students
            WHERE tracking_code = ?
            """,
            (tracking_code.strip().upper(),),
        )

        row = cursor.fetchone()

    return dict(row) if row else None


def get_student_by_telegram_id(
    telegram_id: int,
) -> Optional[dict]:
    """
    دریافت آخرین ثبت‌نام یک کاربر تلگرام.
    """

    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT *
            FROM students
            WHERE telegram_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (telegram_id,),
        )

        row = cursor.fetchone()

    return dict(row) if row else None


def get_all_students() -> list[dict]:
    """
    دریافت همه ثبت‌نام‌ها از جدید به قدیم.
    """

    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT *
            FROM students
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

    return [
        dict(row)
        for row in rows
    ]


def save_signed_contract(
    tracking_code: str,
    file_id: str,
) -> bool:
    """
    ثبت فایل قرارداد امضاشده در دیتابیس.
    """

    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE students
            SET
                signed_contract = ?,
                contract_received = 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE tracking_code = ?
            """,
            (
                file_id,
                tracking_code.strip().upper(),
            ),
        )

        return cursor.rowcount > 0