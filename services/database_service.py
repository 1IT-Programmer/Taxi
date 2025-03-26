from sqlalchemy.exc import SQLAlchemyError
from database.db import Session
from database.models import User, Trip, SupportMessage
from datetime import datetime

def register_user(user_data: dict):
    try:
        session = Session()
        user = User(
            telegram_id=user_data['telegram_id'],
            phone=user_data['phone'],
            full_name=user_data['full_name'],
            role=user_data.get('role', 'passenger')
        )
        session.add(user)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e

def block_user(telegram_id: int) -> bool:
    try:
        session = Session()
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            user.is_blocked = True
            session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        session.rollback()
        raise e

def create_trip(driver_id: int, departure_time: datetime, seats: int, route: str):
    try:
        session = Session()
        trip = Trip(
            driver_id=driver_id,
            departure_time=departure_time,
            seats=seats,
            route=route
        )
        session.add(trip)
        session.commit()
        return trip
    except SQLAlchemyError as e:
        session.rollback()
        raise e

def search_trips(date_str: str):
    try:
        session = Session()
        target_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        return session.query(Trip).filter(
            Trip.departure_time >= target_date,
            Trip.departure_time < target_date.replace(day=target_date.day + 1)
        ).all()
    except Exception as e:
        raise e

def book_seat(trip_id: int, passenger_id: int):
    try:
        session = Session()
        trip = session.query(Trip).get(trip_id)
        if trip.seats > 0:
            trip.seats -= 1
            session.commit()
        else:
            raise ValueError("Нет свободных мест")
    except SQLAlchemyError as e:
        session.rollback()
        raise e

def send_support_message(user_id: int, message: str):
    try:
        session = Session()
        support_message = SupportMessage(
            user_id=user_id,
            message=message
        )
        session.add(support_message)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
