from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from configs.Environment import get_environment_variables

# Runtime Environment Configuration
env = get_environment_variables()

# Generate Database URL
DATABASE_URL = "mysql://root:root@db:3306/db"

# Create Database Engine
Engine = create_engine(
    DATABASE_URL, echo=env.DEBUG_MODE, future=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
        print("Database Connection")
    finally:
        db.close()
