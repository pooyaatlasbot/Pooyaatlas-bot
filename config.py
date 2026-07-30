import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = int(os.getenv("ADMIN_ID", "5679516922"))

SCHOOL_NAME = "آموزشگاه خلبانی پویا فلایت"
WEBSITE = "https://pooyaflight.ir"
PHONE = "09124905605"
ADDRESS = (
    "کرج، بلوار مطهری شمالی، بین خیابان پیروزی و آزادی، "
    "ساختمان وکلا، پلاک ۱۶۶، واحد ۳، جنب هلسی‌لند"
)

DATA_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data")))
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_NAME = Path(
    os.getenv("DATABASE_PATH", str(DATA_DIR / "users.db"))
)

CONTRACT_FILE = Path(
    os.getenv(
        "CONTRACT_FILE",
        str(BASE_DIR / "contracts" / "Contract.pdf"),
    )
)

UPLOAD_DIR = Path(
    os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads"))
)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

TRACKING_PREFIX = "PF"

COURSES = (
    "✈️ دوره مقدماتی UL-PPL",
    "🛫 دوره پیشرفته UL-CPL",
    "👨‍✈️ استاد خلبانی UL-IP",
)
