from sqlalchemy import Column, Integer, ForeignKey #type: ignore
from models import Base #type: ignore

class Exemplar(Base):
    __tablename__ = "exemplar"
    numtombo = Column(Integer, primary_key=True)
    codlivro = Column(Integer, ForeignKey('livro.codlivro'))