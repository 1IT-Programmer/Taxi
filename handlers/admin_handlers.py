from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from services.database_service import block_user, get_user_by_phone
from utils.keyboards import get_admin_keyboard
from config import Config
import logging

logger = logging.getLogger(__name__)
BLOCK_USER = 1

def admin_panel(update: Update, context):
    if update.effective_user.id not in Config.ADMIN_IDS:
        update.message.reply_text("🚫 Доступ запрещен!")
        return ConversationHandler.END
    
    update.message.reply_text(
        "Панель администратора:",
        reply_markup=get_admin_keyboard()
    )
    return ConversationHandler.END

def block_user_start(update: Update, context):
    update.message.reply_text("Введите номер телефона пользователя для блокировки:")
    return BLOCK_USER

def process_block_user(update: Update, context):
    phone = update.message.text
    user = get_user_by_phone(phone)
    
    if user and block_user(user.telegram_id):
        update.message.reply_text(f"✅ Пользователь {phone} заблокирован!")
    else:
        update.message.reply_text("❌ Пользователь не найден!")
    
    return ConversationHandler.END

admin_conversation = ConversationHandler(
    entry_points=[CommandHandler('admin', admin_panel)],
    states={
        BLOCK_USER: [MessageHandler(Filters.text & ~Filters.command, process_block_user)]
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
)
