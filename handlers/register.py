```python
import os
import uuid

from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from database import add_student
from config import ADMIN_ID, CONTRACT_FILE


# =========================================================
# مراحل ثبت نام
# =========================================================

FULL_NAME, PHONE, NATIONAL_CODE, BIRTH_DATE, CITY, COURSE, EDUCATION = range(7)


# =========================================================
# شروع ثبت نام
# =========================================================

async def start_register(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        """
📝 ثبت‌نام در آموزشگاه خلبانی پویا فلایت

لطفاً نام و نام خانوادگی خود را وارد کنید:
"""
    )

    return FULL_NAME


# =========================================================
# دریافت نام و نام خانوادگی
# =========================================================

async def full_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["full_name"] = update.message.text

    await update.message.reply_text(
        """
📱 لطفاً شماره تماس خود را وارد کنید:

مثال:
09123456789
"""
    )

    return PHONE


# =========================================================
# دریافت شماره تماس
# =========================================================

async def phone(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["phone"] = update.message.text

    await update.message.reply_text(
        """
🪪 لطفاً کد ملی خود را وارد کنید:
"""
    )

    return NATIONAL_CODE


# =========================================================
# دریافت کد ملی
# =========================================================

async def national_code(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["national_code"] = update.message.text

    await update.message.reply_text(
        """
📅 لطفاً تاریخ تولد خود را وارد کنید:

مثال:
1370/01/15
"""
    )

    return BIRTH_DATE


# =========================================================
# دریافت تاریخ تولد
# =========================================================

async def birth_date(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["birth_date"] = update.message.text

    await update.message.reply_text(
        """
🏙 لطفاً شهر محل سکونت خود را وارد کنید:
"""
    )

    return CITY


# =========================================================
# دریافت شهر
# =========================================================

async def city(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["city"] = update.message.text

    await update.message.reply_text(
        """
✈️ لطفاً دوره مورد نظر خود را وارد کنید:

مثال:
آموزش خلبانی فوق سبک
"""
    )

    return COURSE


# =========================================================
# دریافت دوره
# =========================================================

async def course(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["course"] = update.message.text

    await update.message.reply_text(
        """
🎓 لطفاً آخرین مدرک تحصیلی خود را وارد کنید:
"""
    )

    return EDUCATION


# =========================================================
# دریافت مدرک تحصیلی و تکمیل ثبت نام
# =========================================================

async def education(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # ذخیره مدرک تحصیلی
    context.user_data["education"] = update.message.text

    # ساخت کد رهگیری
    tracking_code = "PF-" + str(uuid.uuid4())[:8].upper()

    # ذخیره کد رهگیری
    context.user_data["tracking_code"] = tracking_code

    # دریافت اطلاعات ثبت نام کننده
    full_name = context.user_data.get(
        "full_name",
        "ثبت نشده"
    )

    phone_number = context.user_data.get(
        "phone",
        "ثبت نشده"
    )

    national_code_value = context.user_data.get(
        "national_code",
        "ثبت نشده"
    )

    birth_date_value = context.user_data.get(
        "birth_date",
        "ثبت نشده"
    )

    city_value = context.user_data.get(
        "city",
        "ثبت نشده"
    )

    education_value = context.user_data.get(
        "education",
        "ثبت نشده"
    )

    course_value = context.user_data.get(
        "course",
        "ثبت نشده"
    )

    # اطلاعات حساب تلگرام
    telegram_name = (
        update.effective_user.full_name
        if update.effective_user
        else "ثبت نشده"
    )

    telegram_username = (
        f"@{update.effective_user.username}"
        if update.effective_user
        and update.effective_user.username
        else "ندارد"
    )

    telegram_id = (
        update.effective_user.id
        if update.effective_user
        else "ثبت نشده"
    )

    # ذخیره اطلاعات در دیتابیس
    add_student(
        tracking_code=tracking_code,
        full_name=full_name,
        phone=phone_number,
        national_code=national_code_value,
        birth_date=birth_date_value,
        city=city_value,
        education=education_value,
        course=course_value,
        has_flight_experience="خیر",
    )

    # پیام کامل برای ادمین
    admin_text = f"""
🆕 ثبت‌نام جدید در آموزشگاه پویا فلایت

━━━━━━━━━━━━━━━━━━

🆔 کد رهگیری:
{tracking_code}

👤 نام و نام خانوادگی:
{full_name}

📱 شماره تماس ثبت‌نام‌کننده:
{phone_number}

🪪 کد ملی:
{national_code_value}

📅 تاریخ تولد:
{birth_date_value}

🏙 شهر محل سکونت:
{city_value}

🎓 آخرین مدرک تحصیلی:
{education_value}

✈️ دوره انتخابی:
{course_value}

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

    # ارسال اطلاعات برای ادمین
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_text,
    )

    # پیام موفقیت به کاربر
    await update.message.reply_text(
        f"""
✅ ثبت‌نام اولیه شما با موفقیت انجام شد.

━━━━━━━━━━━━━━━━━━

🆔 کد رهگیری:

{tracking_code}

📱 شماره تماس ثبت‌شده:

{phone_number}

━━━━━━━━━━━━━━━━━━

📄 قرارداد آموزشگاه برای شما ارسال می‌شود.

لطفاً قرارداد را دانلود و مطالعه کنید.

✍️ پس از مطالعه و امضا، لطفاً قرارداد امضاشده را به صورت عکس یا فایل PDF از طریق همین ربات ارسال نمایید.

با تشکر
✈️ آموزشگاه خلبانی پویا فلایت
"""
    )

    # ارسال قرارداد
    if os.path.exists(CONTRACT_FILE):

        with open(CONTRACT_FILE, "rb") as pdf:

            await update.message.reply_document(
                document=pdf,
                filename="PooyaFlight-Contract.pdf",
                caption="""
📄 قرارداد آموزشگاه خلبانی پویا فلایت

لطفاً قرارداد را دانلود و مطالعه کنید.

✍️ پس از امضا، قرارداد امضاشده را:

📸 به صورت عکس

یا

📄 به صورت فایل PDF

از طریق همین ربات ارسال نمایید.

با تشکر
✈️ آموزشگاه خلبانی پویا فلایت
"""
            )

    else:

        await update.message.reply_text(
            """
❌ فایل قرارداد روی سرور پیدا نشد.

لطفاً با پشتیبانی آموزشگاه پویا فلایت تماس بگیرید.
"""
        )

    return ConversationHandler.END


# =========================================================
# دریافت قرارداد امضا شده
# =========================================================

async def receive_contract(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    tracking_code = context.user_data.get(
        "tracking_code",
        "ثبت نشده"
    )

    full_name = context.user_data.get(
        "full_name",
        "ثبت نشده"
    )

    phone_number = context.user_data.get(
        "phone",
        "ثبت نشده"
    )

    telegram_id = update.effective_user.id

    telegram_username = (
        f"@{update.effective_user.username}"
        if update.effective_user.username
        else "ندارد"
    )

    # اگر PDF ارسال شده باشد
    if update.message.document:

        document = update.message.document

        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=document.file_id,
            caption=f"""
📄 قرارداد امضا شده جدید

━━━━━━━━━━━━━━━━━━

🆔 کد رهگیری:
{tracking_code}

👤 نام:
{full_name}

📱 شماره تماس:
{phone_number}

🔗 Username:
{telegram_username}

🆔 Telegram ID:
{telegram_id}

━━━━━━━━━━━━━━━━━━

✅ قرارداد توسط ثبت‌نام‌کننده ارسال شد.
"""
        )

    # اگر تصویر قرارداد ارسال شده باشد
    elif update.message.photo:

        photo = update.message.photo[-1]

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo.file_id,
            caption=f"""
📸 تصویر قرارداد امضا شده جدید

━━━━━━━━━━━━━━━━━━

🆔 کد رهگیری:
{tracking_code}

👤 نام:
{full_name}

📱 شماره تماس:
{phone_number}

🔗 Username:
{telegram_username}

🆔 Telegram ID:
{telegram_id}

━━━━━━━━━━━━━━━━━━

✅ قرارداد توسط ثبت‌نام‌کننده ارسال شد.
"""
        )

    # اگر فرمت اشتباه باشد
    else:

        await update.message.reply_text(
            """
❌ فرمت فایل صحیح نیست.

لطفاً قرارداد امضا شده را به صورت:

📸 عکس

یا

📄 فایل PDF

ارسال کنید.
"""
        )

        return

    # پیام موفقیت به کاربر
    await update.message.reply_text(
        """
✅ قرارداد امضا شده شما با موفقیت دریافت شد.

📌 قرارداد برای بررسی به آموزشگاه پویا فلایت ارسال گردید.

⏳ پس از بررسی، نتیجه از طریق همین ربات به شما اطلاع داده خواهد شد.

با تشکر
✈️ آموزشگاه خلبانی پویا فلایت
"""
    )


# =========================================================
# ساخت ConversationHandler ثبت نام
# =========================================================

register_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex("^📝 ثبت‌نام$"),
            start_register
        )
    ],

    states={

        FULL_NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                full_name
            )
        ],

        PHONE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                phone
            )
        ],

        NATIONAL_CODE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                national_code
            )
        ],

        BIRTH_DATE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                birth_date
            )
        ],

        CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                city
            )
        ],

        COURSE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                course
            )
        ],

        EDUCATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                education
            )
        ],
    },

    fallbacks=[],
)
```
