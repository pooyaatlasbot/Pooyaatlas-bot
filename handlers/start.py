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
        resize_keyboard=True,
    )

    await update.message.reply_text(
        """
✈️ به سامانه ثبت‌نام آموزشگاه خلبانی پویا فلایت خوش آمدید.

از منوی زیر یکی از گزینه‌ها را انتخاب کنید.
""",
        reply_markup=reply_markup,
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📞 تماس با مشاور":
        await update.message.reply_text(
            "📞 شماره مشاور:\n09123456789"
        )

    elif text == "💰 شهریه دوره‌ها":
        await update.message.reply_text(
            "برای اطلاع از شهریه با آموزشگاه تماس بگیرید."
        )

    elif text == "📄 قرارداد آموزشی":
        await update.message.reply_text(
            "برای دریافت قرارداد ابتدا ثبت‌نام اولیه را انجام دهید."
        )