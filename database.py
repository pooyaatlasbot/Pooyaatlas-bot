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
            "admin_note": "TEXT DEFAULT ''",
        }
        for column, definition in migrations.items():
            _add_column_if_missing(
                conn, "students", column, definition
            )

        conn.execute("""
            CREATE TABLE IF NOT EXISTS broadcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER NOT NULL,
                message_text TEXT NOT NULL,
                success_count INTEGER DEFAULT 0,
                failed_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

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

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                telegram_id INTEGER NOT NULL,
                receipt_file_id TEXT NOT NULL,
                receipt_file_type TEXT NOT NULL,
                original_name TEXT DEFAULT '',
                mime_type TEXT DEFAULT '',
                status TEXT DEFAULT 'pending',
                reviewed_by INTEGER,
                reviewed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_payments_student
            ON payments(student_id)
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


def search_students(query: str, limit: int = 20) -> list[dict]:
    like = f"%{query.strip()}%"
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM students
            WHERE tracking_code LIKE ? OR full_name LIKE ? OR phone LIKE ?
               OR national_code LIKE ? OR telegram_username LIKE ?
            ORDER BY id DESC LIMIT ?
            """,
            (like, like, like, like, like, limit),
        ).fetchall()
    return [dict(row) for row in rows]


def update_status(tracking_code: str, status: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE students SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE tracking_code = ?
            """,
            (status, tracking_code.strip().upper()),
        )
    return cursor.rowcount > 0


def update_admin_note(tracking_code: str, note: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE students SET admin_note = ?, updated_at = CURRENT_TIMESTAMP
            WHERE tracking_code = ?
            """,
            (note.strip(), tracking_code.strip().upper()),
        )
    return cursor.rowcount > 0


def save_broadcast(
    admin_id: int,
    message_text: str,
    success_count: int,
    failed_count: int,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO broadcasts (
                admin_id, message_text, success_count, failed_count
            ) VALUES (?, ?, ?, ?)
            """,
            (admin_id, message_text, success_count, failed_count),
        )


def create_payment_receipt(
    *,
    student_id: int,
    telegram_id: int,
    file_id: str,
    file_type: str,
    original_name: str = "",
    mime_type: str = "",
) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO payments (
                student_id, telegram_id, receipt_file_id, receipt_file_type,
                original_name, mime_type
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (student_id, telegram_id, file_id, file_type, original_name, mime_type),
        )
        conn.execute(
            """
            UPDATE students SET status = 'رسید پرداخت در انتظار بررسی',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (student_id,),
        )
        return int(cursor.lastrowid)


def get_payment(payment_id: int) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT p.*, s.tracking_code, s.full_name, s.phone, s.course
            FROM payments p
            JOIN students s ON s.id = p.student_id
            WHERE p.id = ?
            """,
            (payment_id,),
        ).fetchone()
    return dict(row) if row else None


def review_payment(payment_id: int, status: str, admin_id: int) -> bool:
    if status not in {'approved', 'rejected'}:
        raise ValueError('Invalid payment status')
    student_status = 'پرداخت تأیید شد' if status == 'approved' else 'پرداخت رد شد'
    with get_connection() as conn:
        payment = conn.execute(
            'SELECT student_id, status FROM payments WHERE id = ?',
            (payment_id,),
        ).fetchone()
        if not payment or payment['status'] != 'pending':
            return False
        cursor = conn.execute(
            """
            UPDATE payments SET status = ?, reviewed_by = ?,
                reviewed_at = CURRENT_TIMESTAMP
            WHERE id = ? AND status = 'pending'
            """,
            (status, admin_id, payment_id),
        )
        if cursor.rowcount:
            conn.execute(
                """
                UPDATE students SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (student_status, payment['student_id']),
            )
        return cursor.rowcount > 0
