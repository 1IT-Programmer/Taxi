from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, Filters, CommandHandler
from services.database_service import register_user
from utils.validators import validate_phone, sanitize_input
from database.db import Session
from database.models import User

REGISTER_PHONE, REGISTER_FULLNAME = range(2)

def start(update, context):
    user_id = update.effective_user.id
    session = Session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if user and user.is_blocked:
        update.message.reply_text("🚫 Ваш аккаунт заблокирован.")
        return ConversationHandler.END
    
    update.message.reply_text(
        "Добро пожаловать! Введите ваш номер телефона:",
        reply_markup=ReplyKeyboardRemove()
    )
    return REGISTER_PHONE

def register_phone(update, context):
    phone = sanitize_input(update.message.text)
    if not validate_phone(phone):
        update.message.reply_text("❌ Неверный формат номера! Попробуйте снова:")
        return REGISTER_PHONE
    
    context.user_data['phone'] = phone
    update.message.reply_text("Введите ваше ФИО:")
    return REGISTER_FULLNAME

def register_fullname(update, context):
    full_name = sanitize_input(update.message.text)
    user_data = {
        'telegram_id': update.effective_user.id,
        'phone': context.user_data['phone'],
        'full_name': full_name,
        'role': 'passenger'
    }
    
    register_user(user_data)
    update.message.reply_text("✅ Регистрация завершена!")
    return ConversationHandler.END

common_conversation = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        REGISTER_PHONE: [MessageHandler(Filters.text & ~Filters.command, register_phone)],
        REGISTER_FULLNAME: [MessageHandler(Filters.text & ~Filters.command, register_fullname)]
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
)