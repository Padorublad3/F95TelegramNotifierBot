from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Entry

engine = create_engine("sqlite:///db.db")
DB_Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return DB_Session()
