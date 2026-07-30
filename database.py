import sqlite3
from typing import Optional

from config import DATABASE_NAME


def get_connection() -> sqlite3.Connection:
    DATABASE_NAME.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(
        str(DATABASE_NAME),
        timeout=30,
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 30000")
    return conn


def _column_names(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {row["name"] for row in rows}


def _add_column_if_missing(
    conn: sqlite3.Connection,
    table: str,
    column: str,
    definition: str,
) -> None:
    if column not in _column_names(conn, table):
        conn.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
        )


def create_database() -> None:
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
                signed_contract_file_id TEXT DEFAULT '',
                signed_contract_type TEXT DEFAULT '',
                contract_received INTEGER DEFAULT 0,
                status TEXT DEFAULT 'ثبت‌نام اولیه',
                register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # مهاجرت امن برای دیتابیس قدیمی
        migrations = {
            "telegram_id": "INTEGER",
            "telegram_username": "TEXT DEFAULT ''",
            "signed_contract_file_id": "TEXT DEFAULT ''",
            "signed_contract_type": "TEXT DEFAULT ''",
            "contract_received": "INTEGER DEFAULT 0",
            "status": "TEXT DEFAULT 'ثبت‌نام اولیه'",
            "updated_at": "TIMESTAMP",
        }
        for column, definition in migrations.items():
            _add_column_if_missing(
                conn, "students", column, definition
            )

        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_students_tracking
            ON students(tracking_code)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_students_telegram
            ON students(telegram_id)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_students_national_code
            ON students(national_code)
            """
        )


def add_student(
    *,
    tracking_code: str,
    telegram_id: Optional[int],
    telegram_username: str,
    full_name: str,
    phone: str,
    national_code: str,
    birth_date: str,
    city: str,
    education: str,
    course: str,
    has_flight_experience: str = "خیر",
) -> int:
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
                has_flight_experience
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            ),
        )
        return int(cursor.lastrowid)


def get_student(tracking_code: str) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM students
            WHERE tracking_code = ?
            """,
            (tracking_code.strip().upper(),),
        ).fetchone()
    return dict(row) if row else None


def get_latest_student_by_telegram_id(
    telegram_id: int,
) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM students
            WHERE telegram_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (telegram_id,),
        ).fetchone()
    return dict(row) if row else None


def get_all_students(limit: int = 100) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM students
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def save_signed_contract(
    *,
    tracking_code: str,
    file_id: str,
    file_type: str,
) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE students
            SET
                signed_contract_file_id = ?,
                signed_contract_type = ?,
                contract_received = 1,
                status = 'قرارداد دریافت شد',
                updated_at = CURRENT_TIMESTAMP
            WHERE tracking_code = ?
            """,
            (
                file_id,
                file_type,
                tracking_code.strip().upper(),
            ),
        )
        return cursor.rowcount > 0


def count_students() -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS count FROM students"
        ).fetchone()
    return int(row["count"])
