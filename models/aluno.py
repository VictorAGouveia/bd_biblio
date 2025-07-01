from sqlalchemy import Column, String, Integer #type: ignore
from models import Base #type: ignore

class Aluno(Base):
    __tablename__ = "aluno"
    matricula = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    curso = Column(String, nullable=False)