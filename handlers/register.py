import os
import uuid

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database import add_student
from config import ADMIN_ID, CONTRACT_FILE


async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["education"] = update.message.text

    tracking_code = "PF-" + str(uuid.uuid4())[:8].upper()

    # ذخیره اطلاعات در دیتابیس
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

    # اطلاعات کامل ثبت نام کننده برای ادمین
    admin_text = f"""
🆕 ثبت‌نام جدید در آموزشگاه پویا فلایت

━━━━━━━━━━━━━━

🆔 کد رهگیری:
{tracking_code}

👤 نام و نام خانوادگی:
{context.user_data["full_name"]}

📱 شماره موبایل:
{context.user_data["phone"]}

🪪 کد ملی:
{context.user_data["national_code"]}

📅 تاریخ تولد:
{context.user_data["birth_date"]}

🏙 شهر محل سکونت:
{context.user_data["city"]}

🎓 آخرین مدرک تحصیلی:
{context.user_data["education"]}

✈️ دوره انتخابی:
{context.user_data["course"]}

👤 نام تلگرام:
{update.effective_user.full_name}

🆔 Telegram ID:
{update.effective_user.id}

━━━━━━━━━━━━━━

✅ ثبت‌نام اولیه با موفقیت انجام شد.
"""

    # ارسال اطلاعات کامل به ادمین
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_text,
    )

    # پیام به ثبت نام کننده
    await update.message.reply_text(
        f"""
✅ ثبت‌نام اولیه شما با موفقیت انجام شد.

🆔 کد رهگیری شما:

{tracking_code}
"""
    )

    # ارسال قرارداد
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