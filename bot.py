import os

from telegram.ext import (
    Application,
    CommandHandler,
)

from handlers.start import start
from handlers.register import register_handler
from handlers.contract import contract_handler

from database import create_database


BOT_TOKEN = os.getenv("BOT_TOKEN")


def main():

    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN تنظیم نشده است.")

    # ساخت دیتابیس
    create_database()

    # ساخت برنامه
    app = Application.builder().token(BOT_TOKEN).build()

    # دستور /start
    app.add_handler(
        CommandHandler("start", start)
    )

    # فرم ثبت نام
    app.add_handler(
        register_handler
    )

    # قرارداد آموزشی
    app.add_handler(
        contract_handler
    )

    print("✈️ Pooya Flight Registration Bot Started Successfully")

    # اجرای ربات
    app.run_polling()


if __name__ == "__main__":
    main()