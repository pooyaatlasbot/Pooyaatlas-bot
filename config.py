import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
def _parse_admin_ids() -> tuple[int, ...]:
    raw = os.getenv("ADMIN_IDS", os.getenv("ADMIN_ID", "5679516922"))
    result = []
    for item in raw.replace(";", ",").split(","):
        item = item.strip()
        if item:
            result.append(int(item))
    return tuple(dict.fromkeys(result))


ADMIN_IDS = _parse_admin_ids()
ADMIN_ID = ADMIN_IDS[0] if ADMIN_IDS else 0

SCHOOL_NAME = "آموزشگاه خلبانی پویا فلایت"
WEBSITE = "https://pooyaflight.ir"
PAYMENT_URL = os.getenv("PAYMENT_URL", "").strip()
PAYMENT_AMOUNT_TEXT = os.getenv("PAYMENT_AMOUNT_TEXT", "مبلغ طبق توافق با آموزشگاه").strip()
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
