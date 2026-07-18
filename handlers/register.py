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

from states import (
    SELECT_COURSE,
    FULL_NAME,
)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🛩 UL-PPL"],
        ["🛫 UL-CPL"],
        ["👨‍✈️ UL-IP"],
    ]

    await update.message.reply_text(
        "لطفاً دوره موردنظر خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return SELECT_COURSE


async def select_course(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["course"] = update.message.text

    await update.message.reply_text(
        "👤 لطفاً نام و نام خانوادگی خود را وارد کنید:"
    )

    return FULL_NAME