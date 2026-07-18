from telegram import (
    Update,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from states import *

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
            one_time_keyboard=True
        )
    )

    return SELECT_COURSE


# -----------------------
# انتخاب دوره
# -----------------------

async def select_course(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["course"] = update.message.text

    await update.message.reply_text(
        "نام و نام خانوادگی خود را وارد کنید:"
    )

    return FULL_NAME


# -----------------------
# نام
# -----------------------

async def full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["full_name"] = update.message.text

    await update.message.reply_text(
        "شماره موبایل:"
    )

    return PHONE


# -----------------------
# موبایل
# -----------------------

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["phone"] = update.message.text

    await update.message.reply_text(
        "کد ملی:"
    )

    return NATIONAL_CODE


# -----------------------
# کد ملی
# -----------------------

async def national_code(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["national_code"] = update.message.text

    await update.message.reply_text(
        "تاریخ تولد:"
    )

    return BIRTH_DATE


# -----------------------
# تاریخ تولد
# -----------------------

async def birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["birth_date"] = update.message.text

    await update.message.reply_text(
        "شهر محل سکونت:"
    )

    return CITY


# -----------------------
# شهر
# -----------------------

async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["city"] = update.message.text

    await update.message.reply_text(
        "آخرین مدرک تحصیلی:"
    )

    return EDUCATION


# -----------------------
# مدرک
# -----------------------

async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["education"] = update.message.text

    await update.message.reply_text(
        "✅ اطلاعات اولیه ثبت شد."
    )

    return ConversationHandler.END


# -----------------------
# لغو
# -----------------------

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "ثبت نام لغو شد."
    )

    return ConversationHandler.END
    
    register_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^✈️ ثبت‌نام دوره‌ها$"),
            register
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
        MessageHandler(filters.Regex("^لغو$"), cancel)
    ],
)