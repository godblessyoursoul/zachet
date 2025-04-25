from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URI = "postgresql+psycopg2://postgres@localhost:5432/postgres"
engine = create_engine(DB_URI, connect_args={"options": "-c search_path=zachet"})

try:
    with engine.connect() as connection:
        print("Получилось!")
except Exception as e:
    print(f"Ошибка подключения: {e}")

Base = declarative_base()
Session = sessionmaker(bind = engine)