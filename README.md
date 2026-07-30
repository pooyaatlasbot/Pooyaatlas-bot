# ربات ثبت‌نام آموزشگاه خلبانی پویا فلایت

## امکانات

- ثبت‌نام مرحله‌ای دوره‌ها
- اعتبارسنجی شماره همراه، کد ملی و تاریخ تولد
- ذخیره اطلاعات و Telegram ID در SQLite
- تولید کد رهگیری
- ارسال مشخصات ثبت‌نام برای مدیر
- ارسال قرارداد آموزشی
- دریافت عکس یا PDF قرارداد امضاشده
- ثبت وضعیت قرارداد در دیتابیس
- پیگیری ثبت‌نام با کد رهگیری
- دستور ساده `/admin` برای مدیر
- مهاجرت خودکار ستون‌های دیتابیس قدیمی

## نصب محلی

Python 3.10 یا بالاتر لازم است.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

در ویندوز:

```bash
.venv\Scripts\activate
```

متغیرهای محیطی را تنظیم کنید:

```bash
export BOT_TOKEN="TOKEN"
export ADMIN_ID="5679516922"
```

سپس:

```bash
python bot.py
```

## قرارداد

فایل قرارداد را دقیقاً در این مسیر قرار دهید:

```text
contracts/Contract.pdf
```

حروف بزرگ و کوچک نام فایل در Railway مهم است.

## Railway

در Variables این موارد را بسازید:

- `BOT_TOKEN`
- `ADMIN_ID`

برای نگهداری دائمی SQLite، یک Volume به مسیر `/data` متصل کنید و متغیر زیر را قرار دهید:

```text
DATA_DIR=/data
```

بدون Volume ممکن است فایل دیتابیس با redeploy از بین برود.

## تست سریع import

```bash
python -c "from handlers.register import register_handler, receive_contract; print('IMPORT OK')"
```

## نکته امنیتی

توکن ربات را داخل کد یا GitHub قرار ندهید.
