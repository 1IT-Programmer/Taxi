from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config

Base = declarative_base()
engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)