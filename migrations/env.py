from database.models import Base  # Добавьте эту строку
from config import Config

# Замените строку с target_metadata на:
target_metadata = Base.metadata

# В функции run_migrations_online() укажите URL БД:
connectable = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    url=Config.DATABASE_URI,  # Используем конфиг из проекта
    poolclass=pool.NullPool,
)
