import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN
from database import create_database
from handlers.admin import admin_handler, error_handler
from handlers.contract import contract_handler
from handlers.register import register_handler, receive_contract
from handlers.start import start, menu


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("متغیر محیطی BOT_TOKEN تنظیم نشده است.")

    create_database()

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .concurrent_updates(False)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_handler))

    app.add_handler(register_handler)
    app.add_handler(contract_handler)

    # فقط عکس یا PDF؛ فایل‌های دیگر قرارداد تلقی نمی‌شوند.
    app.add_handler(
        MessageHandler(
            filters.PHOTO | filters.Document.MimeType("application/pdf"),
            receive_contract,
        )
    )

    # منوی متنی باید پس از ConversationHandlerها باشد.
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, menu)
    )

    app.add_error_handler(error_handler)

    logger.info("Pooya Flight Registration Bot started.")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
