from sqlalchemy import Column, Integer, ForeignKey #type: ignore
from models import Base #type: ignore

class Emp_Exemp(Base):
    __tablename__ = "emp_exemp"
    numtombo = Column(Integer, ForeignKey('exemplar.numtombo'), primary_key=True)
    codempres = Column(Integer, ForeignKey('emprestimo.codempres'))