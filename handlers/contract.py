from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from config import CONTRACT_FILE
import os


async def send_contract(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not os.path.exists(CONTRACT_FILE):
        await update.message.reply_text(
            "❌ فایل قرارداد هنوز روی سرور قرار نگرفته است."
        )
        return

    with open(CONTRACT_FILE, "rb") as pdf:
        await update.message.reply_document(
            document=pdf,
            filename="PooyaFlight-Contract.pdf",
            caption="📄 قرارداد آموزشی آموزشگاه پویا فلایت"
        )


contract_handler = MessageHandler(
    filters.Regex("^📄 قرارداد آموزشی$"),
    send_contract,
)