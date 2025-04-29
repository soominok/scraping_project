from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DB_CONFIG


db_url = {
    f"mysql+mysqlconnector://{MYSQL_CONFIG['user']}:"
        f"{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}/"
            f"{MYSQL_CONFIG['database']}"
}

engine = create_engine(db_url, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)