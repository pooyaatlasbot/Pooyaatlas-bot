     from config import PHONE, WEBSITE

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from telegram.ext import ContextTypes


# =========================================================
# منوی اصلی
# =========================================================

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


# =========================================================
# منوی اصلی
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
                    "💳 پرداخت آنلاین شهریه",
                    url="https://blubiz.sb24.ir/pl/payment-links/fed79061-fd83-4c54-a7a3-2aa35d9e4945?amount=25000000"
                )
            ],
            [
                InlineKeyboardButton(
                    "🧾 ارسال رسید پرداخت",
                    callback_data="send_payment_receipt"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(
            keyboard
        )

        await update.message.reply_text(
            """
💰 پرداخت شهریه آموزشگاه پویا فلایت

💵 مبلغ قابل پرداخت:

۲۵٬۰۰۰٬۰۰۰ ریال

━━━━━━━━━━━━━━━━━━

1️⃣ ابتدا روی دکمه «پرداخت آنلاین شهریه» کلیک کنید.

2️⃣ پرداخت خود را انجام دهید.

3️⃣ سپس روی گزینه «ارسال رسید پرداخت» کلیک کنید.

4️⃣ تصویر یا فایل رسید پرداخت را برای ربات ارسال کنید.

📌 پس از بررسی رسید توسط آموزشگاه، پرداخت شما تأیید خواهد شد.
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
