from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def get_admin_keyboard():
    return ReplyKeyboardMarkup(
        [["Добавить водителя", "Заблокировать пользователя"], ["Статистика"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_driver_keyboard():
    return ReplyKeyboardMarkup(
        [["Создать рейс", "Мои рейсы"], ["Настройки"]],
        resize_keyboard=True
    )

def get_passenger_keyboard():
    return ReplyKeyboardMarkup(
        [["🔍 Поиск рейсов", "🆘 Поддержка"], ["Мои бронирования"]],
        resize_keyboard=True
    )

def get_yes_no_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Да", callback_data="yes"), InlineKeyboardButton("Нет", callback_data="no")]
    ])
