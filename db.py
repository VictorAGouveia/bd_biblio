from sqlalchemy import create_engine #type: ignore
from sqlalchemy.orm import sessionmaker #type: ignore

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/teste_proj1"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)