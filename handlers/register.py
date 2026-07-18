from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from states import (
    SELECT_COURSE,
    FULL_NAME,
    PHONE,
    NATIONAL_CODE,
    BIRTH_DATE,
    CITY,
    EDUCATION,
)

# -----------------------
# شروع ثبت نام
# -----------------------

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["✈️ دوره مقدماتی UL-PPL"],
        ["🛫 دوره پیشرفته UL-CPL"],
        ["👨‍✈️ استاد خلبانی UL-IP"],
    ]

    await update.message.reply_text(
        "لطفاً دوره مورد نظر خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )

    return SELECT_COURSE


# -----------------------
# انتخاب دوره
# -----------------------

async def select_course(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["course"] = update.message.text

    await update.message.reply_text(
        "👤 نام و نام خانوادگی خود را وارد کنید:"
    )

    return FULL_NAME


# -----------------------
# نام و نام خانوادگی
# -----------------------

async def full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["full_name"] = update.message.text

    await update.message.reply_text(
        "📱 شماره موبایل خود را وارد کنید:"
    )

    return PHONE


# -----------------------
# شماره موبایل
# -----------------------

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["phone"] = update.message.text

    await update.message.reply_text(
        "🆔 کد ملی خود را وارد کنید:"
    )

    return NATIONAL_CODE


# -----------------------
# کد ملی
# -----------------------

async def national_code(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["national_code"] = update.message.text

    await update.message.reply_text(
        "📅 تاریخ تولد را وارد کنید:"
    )

    return BIRTH_DATE


# -----------------------
# تاریخ تولد
# -----------------------

async def birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["birth_date"] = update.message.text

    await update.message.reply_text(
        "🏙 شهر محل سکونت را وارد کنید:"
    )

    return CITY


# -----------------------
# شهر
# -----------------------

async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["city"] = update.message.text

    await update.message.reply_text(
        "🎓 آخرین مدرک تحصیلی را وارد کنید:"
    )

    return EDUCATION


# -----------------------
# مدرک تحصیلی
# -----------------------

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["education"] = update.message.text

    await update.message.reply_text(
        "✅ اطلاعات اولیه شما ثبت شد."
    )

    return ConversationHandler.END


# -----------------------
# لغو ثبت نام
# -----------------------

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "❌ ثبت‌نام لغو شد."
    )

    return ConversationHandler.END


# -----------------------
# Conversation Handler
# -----------------------

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