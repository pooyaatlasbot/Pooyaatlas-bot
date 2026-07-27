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

    keyboard = [
        ["✈️ دوره مقدماتی UL-PPL"],
        ["🛫 دوره پیشرفته UL-CPL"],
        ["👨‍✈️ استاد خلبانی UL-IP"],
    ]

    await update.message.reply_text(
        "لطفاً دوره مورد نظر خود را انتخاب کنید:",
        reply_markup=__import__(
            "telegram"
        ).ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
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
        "👤 لطفاً نام و نام خانوادگی خود را وارد کنید:"
    )

    return FULL_NAME


# =========================================================
# دریافت نام
# =========================================================

async def full_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["full_name"] = update.message.text

    await update.message.reply_text(
        "📱 لطفاً شماره تماس خود را وارد کنید:\n\n"
        "مثال:\n"
        "09123456789"
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
        "🪪 لطفاً کد ملی خود را وارد کنید:"
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
        "📅 لطفاً تاریخ تولد خود را وارد کنید:\n\n"
        "مثال:\n"
        "1370/01/15"
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
        "🏙 لطفاً شهر محل سکونت خود را وارد کنید:"
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
        "🎓 لطفاً آخرین مدرک تحصیلی خود را وارد کنید:"
    )

    return EDUCATION


# =========================================================
# دریافت مدرک و تکمیل ثبت نام
# =========================================================

async def education(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["education"] = update.message.text

    # ساخت کد رهگیری
    tracking_code = (
        "PF-" +
        str(uuid.uuid4())[:8].upper()
    )

    context.user_data["tracking_code"] = tracking_code

    # =====================================================
    # اطلاعات ثبت نام کننده
    # =====================================================

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

    # =====================================================
    # اطلاعات تلگرام
    # =====================================================

    telegram_name = "ثبت نشده"
    telegram_username = "ندارد"
    telegram_id = "ثبت نشده"

    if update.effective_user:

        telegram_name = (
            update.effective_user.full_name
        )

        telegram_id = (
            update.effective_user.id
        )

        if update.effective_user.username:

            telegram_username = (
                "@"
                + update.effective_user.username
            )

    # =====================================================
    # ذخیره در دیتابیس
    # =====================================================

    try:

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

    except Exception as e:

        print(
            "DATABASE ERROR:",
            e
        )

        await update.message.reply_text(
            "❌ خطایی در ذخیره اطلاعات ثبت‌نام رخ داد.\n"
            "لطفاً دوباره تلاش کنید."
        )

        return ConversationHandler.END

    # =====================================================
    # پیام کامل برای ادمین
    # =====================================================

    admin_text = f"""
🆕 ثبت‌نام جدید
✈️ آموزشگاه خلبانی پویا فلایت

━━━━━━━━━━━━━━━━━━

🆔 کد رهگیری:
{tracking_code}

👤 نام و نام خانوادگی:
{full_name}

📱 شماره تماس:
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

👤 نام تلگرام:
{telegram_name}

🔗 Username:
{telegram_username}

🆔 Telegram ID:
{telegram_id}

━━━━━━━━━━━━━━━━━━

✅ اطلاعات ثبت‌نام در دیتابیس ذخیره شد.
"""

    # =====================================================
    # ارسال اطلاعات کامل برای ادمین
    # =====================================================

    try:

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
        )

    except Exception as e:

        print(
            "ADMIN MESSAGE ERROR:",
            e
        )

    # =====================================================
    # پیام موفقیت برای متقاضی
    # =====================================================

    await update.message.reply_text(
        f"""
✅ ثبت‌نام اولیه شما با موفقیت انجام شد.

━━━━━━━━━━━━━━━━━━

🆔 کد رهگیری شما:

{tracking_code}

📱 شماره تماس ثبت‌شده:

{phone_number}

━━━━━━━━━━━━━━━━━━

📄 قرارداد آموزشی برای شما ارسال می‌شود.

لطفاً قرارداد را دانلود، مطالعه و امضا کنید.

✍️ سپس قرارداد امضاشده را به صورت عکس یا فایل PDF
از طریق همین ربات ارسال نمایید.

✈️ آموزشگاه خلبانی پویا فلایت
"""
    )

    # =====================================================
    # ارسال قرارداد
    # =====================================================

    if os.path.exists(CONTRACT_FILE):

        try:

            with open(
                CONTRACT_FILE,
                "rb"
            ) as pdf:

                await update.message.reply_document(
                    document=pdf,
                    filename="PooyaFlight-Contract.pdf",
                    caption="""
📄 قرارداد آموزشی
آموزشگاه خلبانی پویا فلایت

لطفاً قرارداد را دانلود و مطالعه کنید.

✍️ پس از امضا، قرارداد امضاشده را:

📸 به صورت عکس

یا

📄 به صورت فایل PDF

از طریق همین ربات ارسال نمایید.
"""
                )

        except Exception as e:

            print(
                "CONTRACT ERROR:",
                e
            )

    else:

        await update.message.reply_text(
            "❌ فایل قرارداد روی سرور پیدا نشد."
        )

    return ConversationHandler.END


# =========================================================
# لغو ثبت نام
# =========================================================

async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "❌ ثبت‌نام لغو شد."
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

    telegram_id = (
        update.effective_user.id
        if update.effective_user
        else "ثبت نشده"
    )

    telegram_username = "ندارد"

    if (
        update.effective_user
        and update.effective_user.username
    ):

        telegram_username = (
            "@"
            + update.effective_user.username
        )

    caption = f"""
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

    # PDF
    if update.message.document:

        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=update.message.document.file_id,
            caption=caption,
        )

    # عکس
    elif update.message.photo:

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption,
        )

    else:

        await update.message.reply_text(
            "❌ لطفاً قرارداد را به صورت عکس یا فایل PDF ارسال کنید."
        )

        return

    await update.message.reply_text(
        """
✅ قرارداد امضاشده شما با موفقیت دریافت شد.

📌 قرارداد برای آموزشگاه پویا فلایت ارسال شد.

⏳ پس از بررسی با شما تماس خواهیم گرفت.

✈️ با تشکر
آموزشگاه خلبانی پویا فلایت
"""
    )


# =========================================================
# Conversation Handler
# =========================================================

register_handler = ConversationHandler(

    entry_points=[

        MessageHandler(
            filters.Regex(
                "^✈️ ثبت نام دوره‌ها$"
            ),
            start_register,
        )

    ],

    states={

        COURSE: [

            MessageHandler(
                filters.TEXT
                & ~filters.COMMAND,
                course,
            )

        ],

        FULL_NAME: [

            MessageHandler(
                filters.TEXT
                & ~filters.COMMAND,
                full_name,
            )

        ],

        PHONE: [

            MessageHandler(
                filters.TEXT
                & ~filters.COMMAND,
                phone,
            )

        ],

        NATIONAL_CODE: [

            MessageHandler(
                filters.TEXT
                & ~filters.COMMAND,
                national_code,
            )

        ],

        BIRTH_DATE: [

            MessageHandler(
                filters.TEXT
                & ~filters.COMMAND,
                birth_date,
            )

        ],

        CITY: [

            MessageHandler(
                filters.TEXT
                & ~filters.COMMAND,
                city,
            )

        ],

        EDUCATION: [

            MessageHandler(
                filters.TEXT
                & ~filters.COMMAND,
                education,
            )

        ],

    },

    fallbacks=[

        MessageHandler(
            filters.Regex("^لغو$"),
            cancel,
        )

    ],

)
