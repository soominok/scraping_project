from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from db_models import Base
from config import SQLALCHEMY_DATABASE_URI
import logging

logger = logging.getLogger(__name__)

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_size=20,
    pool_pre_ping=True,
    max_overflow=100
)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db_session():
    session = SessionLocal()
    try:
        yield session
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()
