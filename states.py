from telegram.ext import ConversationHandler

(
    SELECT_COURSE,
    FULL_NAME,
    PHONE,
    NATIONAL_CODE,
    BIRTH_DATE,
    CITY,
    EDUCATION,
    FLIGHT_EXPERIENCE,
    CONTRACT,
    PHOTO,
    NATIONAL_CARD,
    BIRTH_CERTIFICATE,
    EDUCATION_FILE,
    MEDICAL_FILE,
    CONFIRM
) = range(15)

END = ConversationHandler.END