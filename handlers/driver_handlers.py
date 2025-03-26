from telegram import Update
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    Filters,
    CommandHandler
)
from services.database_service import create_trip, get_user_role
from utils.validators import validate_date, validate_time, validate_seats, sanitize_input
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
DEPARTURE_DATE, DEPARTURE_TIME, SEATS, ROUTE = range(4)

def start_create_trip(update: Update, context):
    user_id = update.effective_user.id
    if get_user_role(user_id) != "driver":
        update.message.reply_text("🚫 Только для водителей!")
        return ConversationHandler.END
    
    update.message.reply_text("Введите дату отправки (ДД.ММ.ГГГГ):")
    return DEPARTURE_DATE

def process_departure_date(update: Update, context):
    date_str = sanitize_input(update.message.text)
    if not validate_date(date_str):
        update.message.reply_text("❌ Неверный формат даты!")
        return DEPARTURE_DATE
    
    context.user_data['date'] = date_str
    update.message.reply_text("Введите время отправки (ЧЧ:ММ):")
    return DEPARTURE_TIME

def process_departure_time(update: Update, context):
    time_str = sanitize_input(update.message.text)
    if not validate_time(time_str):
        update.message.reply_text("❌ Неверный формат времени!")
        return DEPARTURE_TIME
    
    try:
        full_datetime = datetime.strptime(
            f"{context.user_data['date']} {time_str}", 
            "%d.%m.%Y %H:%M"
        )
        context.user_data['departure_time'] = full_datetime
        update.message.reply_text("Введите количество мест:")
        return SEATS
    except Exception as e:
        logger.error(f"Ошибка времени: {e}")
        update.message.reply_text("⚠ Ошибка! Начните заново.")
        return ConversationHandler.END

def process_seats(update: Update, context):
    seats = sanitize_input(update.message.text)
    if not validate_seats(seats):
        update.message.reply_text("❌ Введите число от 1 до 10!")
        return SEATS
    
    context.user_data['seats'] = int(seats)
    update.message.reply_text("Введите маршрут (например, Москва-Санкт-Петербург):")
    return ROUTE

def process_route(update: Update, context):
    route = sanitize_input(update.message.text)
    try:
        create_trip(
            driver_id=update.effective_user.id,
            departure_time=context.user_data['departure_time'],
            seats=context.user_data['seats'],
            route=route
        )
        update.message.reply_text("✅ Рейс успешно создан!")
    except Exception as e:
        logger.error(f"Ошибка создания рейса: {e}")
        update.message.reply_text("⚠ Ошибка при создании рейса!")
    
    return ConversationHandler.END

driver_conversation = ConversationHandler(
    entry_points=[CommandHandler('create_trip', start_create_trip)],
    states={
        DEPARTURE_DATE: [MessageHandler(Filters.text, process_departure_date)],
        DEPARTURE_TIME: [MessageHandler(Filters.text, process_departure_time)],
        SEATS: [MessageHandler(Filters.text, process_seats)],
        ROUTE: [MessageHandler(Filters.text, process_route)]
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
)