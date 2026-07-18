from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import uuid
import os

from config import ADMIN_ID
from config import CONTRACT_FILE

from database import add_student

from states import (
    SELECT_COURSE,
    FULL_NAME,
    PHONE,
    NATIONAL_CODE,
    BIRTH_DATE,
    CITY,
    EDUCATION,
)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["✈️ دوره مقدماتی UL-PPL"],
        ["🛫 دوره پیشرفته UL-CPL"],
        ["👨‍✈️ استاد خلبانی UL-IP"],
    ]

    await update.message.reply_text(
        "لطفاً دوره مورد نظر خود را انتخاب کنید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )

    return SELECT_COURSE


async def select_course(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["course"] = update.message.text

    await update.message.reply_text(
        "👤 نام و نام خانوادگی:"
    )

    return FULL_NAME


async def full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["full_name"] = update.message.text

    await update.message.reply_text(
        "📱 شماره موبایل:"
    )

    return PHONE


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["phone"] = update.message.text

    await update.message.reply_text(
        "🪪 کد ملی:"
    )

    return NATIONAL_CODE


async def national_code(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["national_code"] = update.message.text

    await update.message.reply_text(
        "📅 تاریخ تولد:"
    )

    return BIRTH_DATE


async def birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["birth_date"] = update.message.text

    await update.message.reply_text(
        "🏙 شهر محل سکونت:"
    )

    return CITY


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["city"] = update.message.text

    await update.message.reply_text(
        "🎓 آخرین مدرک تحصیلی:"
    )

    return EDUCATION

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["education"] = update.message.text

    tracking_code = "PF-" + str(uuid.uuid4())[:8].upper()

    add_student(
        tracking_code=tracking_code,
        full_name=context.user_data["full_name"],
        phone=context.user_data["phone"],
        national_code=context.user_data["national_code"],
        birth_date=context.user_data["birth_date"],
        city=context.user_data["city"],
        education=context.user_data["education"],
        course=context.user_data["course"],
        has_flight_experience="خیر",
    )

    await update.message.reply_text(
        f"""
✅ ثبت‌نام اولیه شما با موفقیت انجام شد.

🆔 کد رهگیری شما:

{tracking_code}
"""
    )

    if os.path.exists(CONTRACT_FILE):

        with open(CONTRACT_FILE, "rb") as pdf:

            await update.message.reply_document(
                document=pdf,
                filename="PooyaFlight-Contract.pdf",
                caption="""
📄 قرارداد آموزشگاه پویا فلایت

لطفاً قرارداد را دانلود کنید.

پس از مطالعه و امضا، فایل یا عکس قرارداد امضا شده را از طریق همین ربات ارسال نمایید.

با تشکر
آموزشگاه خلبانی پویا فلایت
"""
            )

    else:

        await update.message.reply_text(
            "❌ فایل قرارداد روی سرور پیدا نشد."
        )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❌ ثبت‌نام لغو شد."
    )

    return ConversationHandler.END


# 👇 اینجا اضافه کن
async def receive_contract(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    text = f"""
📄 قرارداد جدید دریافت شد

👤 نام:
{user.full_name}

🆔 آیدی:
{user.id}
"""

    if update.message.document:

        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=update.message.document.file_id,
            caption=text,
        )

    elif update.message.photo:

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=text,
        )

    await update.message.reply_text(
        "✅ قرارداد شما با موفقیت دریافت شد.\n\nپس از بررسی با شما تماس خواهیم گرفت."
    )

register_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^✈️ ثبت نام دوره‌ها$"),
            register,
        )
    ],
    states={
        SELECT_COURSE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, select_course)
        ],
        FULL_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, full_name)
        ],
        PHONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, phone)
        ],
        NATIONAL_CODE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, national_code)
        ],
        BIRTH_DATE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, birth_date)
        ],
        CITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, city)
        ],
        EDUCATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, education)
        ],
    },
    fallbacks=[
        MessageHandler(
            filters.Regex("^لغو$"),
            cancel,
        )
    ],
)