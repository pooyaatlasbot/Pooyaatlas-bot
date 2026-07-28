  from config import PHONE, WEBSITE

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import ContextTypes


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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


async def menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    # ==========================
    # تماس با مشاور
    # ==========================

    if text == "📞 تماس با مشاور":

        await update.message.reply_text(
            f"""
📞 تماس با مشاور

☎️ شماره تماس:
{PHONE}

🌐 وب‌سایت:
{WEBSITE}

در ساعات اداری پاسخگوی شما هستیم.
"""
        )

    # ==========================
    # شهریه
    # ==========================

    elif text == "💰 شهریه دوره‌ها":

        keyboard = [
            [
                InlineKeyboardButton(
                    "💳 پرداخت شهریه",
                    url="https://blubiz.sb24.ir/pl/payment-links/fed79061-fd83-4c54-a7a3-2aa35d9e4945?amount=25000000"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            """
💰 شهریه دوره

💵 مبلغ قابل پرداخت:
۲۵٬۰۰۰٬۰۰۰ تومان

برای پرداخت آنلاین روی دکمه زیر کلیک کنید:

👇 پرداخت امن شهریه
""",
            reply_markup=reply_markup,
        )

    # ==========================
    # قرارداد
    # ==========================

    elif text == "📄 قرارداد آموزشی":

        await update.message.reply_text(
            "برای دریافت قرارداد ابتدا ثبت‌نام اولیه را انجام دهید."
        )
