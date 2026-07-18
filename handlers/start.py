from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["✈️ ثبت نام دوره‌ها"],
        ["📄 قرارداد آموزشی"],
        ["💰 شهریه دوره‌ها"],
        ["📞 تماس با مشاور"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        f"""
✈️ به سامانه ثبت‌نام آموزشگاه خلبانی پویا فلایت خوش آمدید.

از منوی زیر یکی از گزینه‌ها را انتخاب کنید.
        """,
        reply_markup=reply_markup
    )