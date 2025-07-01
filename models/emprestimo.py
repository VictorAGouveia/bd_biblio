from sqlalchemy import Column, Integer, String, ForeignKey #type: ignore
from models import Base #type: ignore

class Emprestimo(Base):
    __tablename__ = "emprestimo"
    codempres = Column(Integer, primary_key=True)
    matricula = Column(Integer, ForeignKey('aluno.matricula'))
    data_emp = Column(String, nullable=False)
    data_prev = Column(String, nullable=False)
    data_dev = Column(String)
    atraso = Column(Integer)