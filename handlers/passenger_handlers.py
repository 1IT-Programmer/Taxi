from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from services.database_service import (
    search_trips,
    book_seat,
    get_trip_details,
    get_user_by_id,
    send_support_message,
)
from utils.validators import validate_date, sanitize_input
from utils.keyboards import get_passenger_keyboard
from config import Config
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

SEARCH_DATE, SELECT_TRIP, CONFIRM_BOOKING, SUPPORT_MESSAGE = range(4)

def start_passenger(update: Update, context):
    update.message.reply_text(
        "Выберите действие:",
        reply_markup=get_passenger_keyboard()
    )
    return ConversationHandler.END

def search_trips_command(update: Update, context):
    update.message.reply_text("Введите дату поездки в формате ДД.ММ.ГГГГ:")
    return SEARCH_DATE

def process_search_date(update: Update, context):
    date_str = sanitize_input(update.message.text)
    
    if not validate_date(date_str):
        update.message.reply_text("❌ Неверный формат даты! Попробуйте снова:")
        return SEARCH_DATE

    try:
        trips = search_trips(date_str)
        if not trips:
            update.message.reply_text("🚫 Рейсов на эту дату не найдено.")
            return ConversationHandler.END

        keyboard = [
            [InlineKeyboardButton(
                f"{trip.route} | {trip.departure_time.strftime('%d.%m %H:%M')}",
                callback_data=f"trip_{trip.id}"
            )] 
            for trip in trips
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text("📅 Доступные рейсы:", reply_markup=reply_markup)
        return SELECT_TRIP

    except Exception as e:
        logger.error(f"Ошибка поиска: {e}")
        update.message.reply_text("⚠ Произошла ошибка. Попробуйте позже.")
        return ConversationHandler.END

def select_trip(update: Update, context):
    query = update.callback_query
    trip_id = int(query.data.split("_")[1])
    context.user_data["trip_id"] = trip_id
    
    trip = get_trip_details(trip_id)
    if trip.seats <= 0:
        query.edit_message_text("😞 Все места уже заняты.")
        return ConversationHandler.END

    driver = get_user_by_id(trip.driver_id)
    message = (
        f"🚗 Рейс: {trip.route}\n"
        f"⏰ Время отправки: {trip.departure_time.strftime('%d.%m.%Y %H:%M')}\n"
        f"👤 Водитель: {driver.full_name}\n"
        f"📞 Контакт: {driver.phone}\n"
        f"🪑 Свободные места: {trip.seats}\n\n"
        "Подтвердите бронирование:"
    )
    
    keyboard = [
        [InlineKeyboardButton("✅ Забронировать", callback_data="confirm_yes")],
        [InlineKeyboardButton("❌ Отмена", callback_data="confirm_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(message, reply_markup=reply_markup)
    return CONFIRM_BOOKING

def confirm_booking(update: Update, context):
    query = update.callback_query
    if query.data == "confirm_yes":
        trip_id = context.user_data["trip_id"]
        user_id = update.effective_user.id
        
        try:
            book_seat(trip_id, user_id)
            query.edit_message_text("🎉 Место успешно забронировано!")
        except Exception as e:
            logger.error(f"Ошибка бронирования: {e}")
            query.edit_message_text("⚠ Не удалось забронировать место.")
    else:
        query.edit_message_text("❌ Бронирование отменено.")
    
    return ConversationHandler.END

def start_support(update: Update, context):
    update.message.reply_text("✍️ Опишите вашу проблему:")
    return SUPPORT_MESSAGE

def process_support(update: Update, context):
    message = sanitize_input(update.message.text)
    user_id = update.effective_user.id
    
    try:
        send_support_message(user_id, message)
        for admin_id in Config.ADMIN_IDS:
            context.bot.send_message(
                admin_id,
                f"🆘 Новое обращение от пользователя {user_id}:\n\n{message}"
            )
        update.message.reply_text("📩 Ваше сообщение отправлено администраторам.")
    except Exception as e:
        logger.error(f"Ошибка поддержки: {e}")
        update.message.reply_text("⚠ Не удалось отправить сообщение.")
    
    return ConversationHandler.END

passenger_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("menu", start_passenger),
        CommandHandler("search", search_trips_command),
        CommandHandler("support", start_support)
    ],
    states={
        SEARCH_DATE: [MessageHandler(Filters.text & ~Filters.command, process_search_date)],
        SELECT_TRIP: [CallbackQueryHandler(select_trip)],
        CONFIRM_BOOKING: [CallbackQueryHandler(confirm_booking)],
        SUPPORT_MESSAGE: [MessageHandler(Filters.text & ~Filters.command, process_support)]
    },
    fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)]
)