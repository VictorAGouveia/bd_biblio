from sqlalchemy import Column, String, Integer #type: ignore
from models import Base #type: ignore

class Livro(Base):
    __tablename__ = "livro"
    codlivro = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    editora = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)