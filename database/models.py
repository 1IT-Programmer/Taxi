from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    role = Column(String(20))
    phone = Column(String(20))
    full_name = Column(String(100))
    is_blocked = Column(Boolean, default=False)
    car_model = Column(String(50))
    car_color = Column(String(20))
    car_number = Column(String(20))

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey("users.id"))
    departure_time = Column(DateTime)
    seats = Column(Integer)
    route = Column(String(100))
    driver = relationship("User", backref="trips")

class SupportMessage(Base):
    __tablename__ = "support_messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("User", backref="support_messages")