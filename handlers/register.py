```python
import os
import uuid

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database import add_student
from config import ADMIN_ID, CONTRACT_FILE


async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ذخیره آخرین مدرک تحصیلی
    context.user_data["education"] = update.message.text

    # ساخت کد رهگیری
    tracking_code = "PF-" + str(uuid.uuid4())[:8].upper()

    # ذخیره کد رهگیری برای استفاده در مراحل بعدی
    context.user_data["tracking_code"] = tracking_code

    # دریافت اطلاعات ثبت نام کننده
    full_name = context.user_data.get("full_name", "ثبت نشده")
    phone = context.user_data.get("phone", "ثبت نشده")
    national_code = context.user_data.get("national_code", "ثبت نشده")
    birth_date = context.user_data.get("birth_date", "ثبت نشده")
    city = context.user_data.get("city", "ثبت نشده")
    education = context.user_data.get("education", "ثبت نشده")
    course = context.user_data.get("course", "ثبت نشده")

    # اطلاعات حساب تلگرام
    telegram_name = update.effective_user.full_name

    telegram_username = (
        f"@{update.effective_user.username}"
        if update.effective_user.username
        else "ندارد"
    )

    telegram_id = update.effective_user.id

    # ذخیره اطلاعات در دیتابیس
    add_student(
        tracking_code=tracking_code,
        full_name=full_name,
        phone=phone,
        national_code=national_code,
        birth_date=birth_date,
        city=city,
        education=education,
        course=course,
        has_flight_experience="خیر",
    )

    # اطلاعات کامل ثبت نام کننده برای ادمین
    admin_text = f"""
🆕 ثبت‌نام جدید در آموزشگاه پویا فلایت

━━━━━━━━━━━━━━━━━━

🆔 کد رهگیری:
{tracking_code}

👤 نام و نام خانوادگی:
{full_name}

📱 شماره تماس ثبت‌نام‌کننده:
{phone}

🪪 کد ملی:
{national_code}

📅 تاریخ تولد:
{birth_date}

🏙 شهر محل سکونت:
{city}

🎓 آخرین مدرک تحصیلی:
{education}

✈️ دوره انتخابی:
{course}

━━━━━━━━━━━━━━━━━━

📱 اطلاعات حساب تلگرام

👤 نام:
{telegram_name}

🔗 نام کاربری:
{telegram_username}

🆔 Telegram ID:
{telegram_id}

━━━━━━━━━━━━━━━━━━

✅ ثبت‌نام اولیه با موفقیت انجام شد.
"""

    # ارسال اطلاعات کامل برای ادمین
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_text,
    )

    # پیام به ثبت نام کننده
    await update.message.reply_text(
        f"""
✅ ثبت‌نام اولیه شما با موفقیت انجام شد.

━━━━━━━━━━━━━━━━━━

🆔 کد رهگیری شما:

{tracking_code}

📱 شماره تماس ثبت‌شده:

{phone}

━━━━━━━━━━━━━━━━━━

📄 اکنون قرارداد آموزشگاه برای شما ارسال می‌شود.

لطفاً قرارداد را دانلود و مطالعه کنید.

✍️ پس از مطالعه و امضا، لطفاً عکس یا فایل PDF قرارداد امضاشده را از طریق همین ربات ارسال نمایید.

با تشکر
✈️ آموزشگاه خلبانی پویا فلایت
"""
    )

    # بررسی وجود فایل قرارداد
    if os.path.exists(CONTRACT_FILE):

        # باز کردن فایل قرارداد
        with open(CONTRACT_FILE, "rb") as pdf:

            # ارسال قرارداد برای کاربر
            await update.message.reply_document(
                document=pdf,
                filename="PooyaFlight-Contract.pdf",
                caption="""
📄 قرارداد آموزشگاه خلبانی پویا فلایت

لطفاً قرارداد را دانلود و مطالعه کنید.

✍️ پس از امضا، لطفاً قرارداد امضاشده را:

📸 به صورت عکس

یا

📄 به صورت فایل PDF

از طریق همین ربات ارسال نمایید.

با تشکر
✈️ آموزشگاه خلبانی پویا فلایت
"""
            )

    else:

        # اگر فایل قرارداد پیدا نشد
        await update.message.reply_text(
            """
❌ فایل قرارداد روی سرور پیدا نشد.

لطفاً با پشتیبانی آموزشگاه پویا فلایت تماس بگیرید.
"""
        )

    # پایان مرحله فعلی
    return ConversationHandler.END
```
