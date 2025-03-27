                    Инструкция по установке и настройке


   1.Установите Python 3.10+:


   2.Клонируйте репозиторий:

bash

git clone https://github.com/1IT-Programmer/Taxi.git

cd project

   3.Установите зависимости:

bash

pip install -r requirements.txt

   4.Настройте переменные окружения:

Создайте файл .env в корне проекта:

BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BOTFATHER
ADMIN_IDS=123456789,987654321
DATABASE_URL=sqlite:///database.db

   5.Инициализируйте Alembic:

bash

alembic init migrations

Замените содержимое migrations/env.py на этот шаблон.

   6.Создайте и примените миграции:

bash

alembic revision --autogenerate -m "Initial tables"
alembic upgrade head

   7.Запустите бота:

bash

python bot.py
