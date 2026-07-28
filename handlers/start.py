from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from telegram.ext import ContextTypes

from config import PHONE, WEBSITE


# =========================================================
# منوی اصلی ربات
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [
        ["✈️ ثبت نام دوره‌ها"],
        ["📄 قرارداد آموزشی"],
        ["💰 شهریه دوره‌ها"],
        ["💳 پرداخت شهریه"],
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


# =========================================================
# مدیریت گزینه‌های منوی اصلی
# =========================================================

async def menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text


    # =====================================================
    # تماس با مشاور
    # =====================================================

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


    # =====================================================
    # شهریه دوره‌ها
    # =====================================================

    elif text == "💰 شهریه دوره‌ها":

        keyboard = [
            [
                InlineKeyboardButton(
                    "💳 پرداخت شهریه - ۲۵ میلیون تومان",
                    url="https://blubiz.sb24.ir/pl/payment-links/fed79061-fd83-4c54-a7a3-2aa35d9e4945?amount=25000000"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(
            keyboard
        )

        await update.message.reply_text(
            """
💰 شهریه دوره‌ها

برای اطلاع از شهریه و پرداخت آنلاین، روی دکمه زیر کلیک کنید.

💳 مبلغ قابل پرداخت:
۲۵٬۰۰۰٬۰۰۰ تومان
""",
            reply_markup=reply_markup,
        )


    # =====================================================
    # پرداخت شهریه
    # =====================================================

    elif text == "💳 پرداخت شهریه":

        keyboard = [
            [
                InlineKeyboardButton(
                    "💳 پرداخت ۲۵٬۰۰۰٬۰۰۰ تومان",
                    url="https://blubiz.sb24.ir/pl/payment-links/fed79061-fd83-4c54-a7a3-2aa35d9e4945?amount=25000000"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(
            keyboard
        )

        await update.message.reply_text(
            """
💳 پرداخت شهریه

مبلغ پرداخت:
۲۵٬۰۰۰٬۰۰۰ تومان

برای ورود به صفحه پرداخت روی دکمه زیر کلیک کنید:
""",
            reply_markup=reply_markup,
        )


    # =====================================================
    # قرارداد آموزشی
    # =====================================================

    elif text == "📄 قرارداد آموزشی":

        await update.message.reply_text(
            "برای دریافت قرارداد ابتدا ثبت‌نام اولیه را انجام دهید."
        )
