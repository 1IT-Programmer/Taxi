from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackContext
from handlers import (
    admin_handlers,
    driver_handlers,
    passenger_handlers,
    common_handlers
)
from config import Config
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def error_handler(update: object, context: CallbackContext):
    logger.error(f"Ошибка: {context.error}")
    if update and hasattr(update, 'message'):
        update.message.reply_text("⚠ Произошла ошибка. Попробуйте позже.")

def main():
    updater = Updater(token=Config.BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(common_handlers.common_conversation)
    dp.add_handler(admin_handlers.admin_conversation())
    dp.add_handler(driver_handlers.driver_conversation())
    dp.add_handler(passenger_handlers.passenger_conversation)
    
    dp.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
