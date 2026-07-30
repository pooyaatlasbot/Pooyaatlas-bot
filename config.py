import os
from pathlib import Path


# =========================================================
# مسیر اصلی پروژه
# =========================================================

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# Telegram Bot
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "متغیر محیطی BOT_TOKEN تنظیم نشده است."
    )


# =========================================================
# Flight School Information
# =========================================================

SCHOOL_NAME = "آموزشگاه خلبانی پویا فلایت"

WEBSITE = "https://pooyaflight.ir"

PHONE = "09124905605"

ADDRESS = (
    "کرج، بلوار مطهری شمالی، بین خیابان پیروزی و آزادی، "
    "ساختمان وکلا، پلاک ۱۶۶، واحد ۳، جنب هلسی لند"
)


# =========================================================
# Admin
# =========================================================

ADMIN_ID_RAW = os.getenv(
    "ADMIN_ID",
    "5679516922",
)

try:
    ADMIN_ID = int(ADMIN_ID_RAW)
except ValueError as exc:
    raise RuntimeError(
        "ADMIN_ID باید یک شناسه عددی معتبر تلگرام باشد."
    ) from exc


# =========================================================
# Database
# =========================================================

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_NAME = DATABASE_DIR / "users.db"


# =========================================================
# Contracts
# =========================================================

CONTRACT_DIR = BASE_DIR / "contracts"

CONTRACT_FILE = CONTRACT_DIR / "Contract.pdf"


# =========================================================
# Upload Folders
# =========================================================

UPLOAD_DIR = BASE_DIR / "uploads"

PHOTO_FOLDER = UPLOAD_DIR / "photos"
NATIONAL_CARD_FOLDER = UPLOAD_DIR / "national_cards"
BIRTH_CERTIFICATE_FOLDER = UPLOAD_DIR / "birth_certificates"
EDUCATION_FOLDER = UPLOAD_DIR / "education"


for folder in (
    PHOTO_FOLDER,
    NATIONAL_CARD_FOLDER,
    BIRTH_CERTIFICATE_FOLDER,
    EDUCATION_FOLDER,
):
    folder.mkdir(
        parents=True,
        exist_ok=True,
    )


# =========================================================
# Tracking Code
# =========================================================

TRACKING_PREFIX = "PF"