from db import engine, SessionLocal
# Importa a engine do arquivo db.py
# LEMBRE DE ALTERAR AS CONFIGURACOES DENTRO DE db.py

# importa os modelos e a base
from models.aluno import Aluno
from models.livro import Livro
from models.emprestimo import Emprestimo
from models.exemplar import Exemplar
from models.emp_exemp import Emp_Exemp
from models import Base #type: ignore

def criar_tabelas_no_postgres():
    # Conecta no banco de dados PostgreSQL e cria as tabelas
    print("Iniciando a criacao das tabelas no banco de dados PostgreSQL...")
    try:
        # tenta criar as tabelas no postgresql
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso (se ainda nao existiam).")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar criar as tabelas: {e}")

if __name__ == "__main__":
    # Garante que a funcao so sera chamada quando o script for executado diretamente
    criar_tabelas_no_postgres()

# abaixo serao criados alguns objetos exemplares para executar os testes
import services.aluno_services as aluno_s
import services.livro_services as livro_s
import services.emprestimo_services as emprestimo_s
import services.exemplar_services as exemplar_s
import services.emp_exemp_services as emp_exemp_s

session = SessionLocal()

aluno_s.criar_aluno(session, 'Jorge S', 1234, 'jorge123@gmail.com', 'Computacao')
aluno_s.criar_aluno(session, 'Claudia B', 1235, 'claudinha@outlook.com', 'Medicina')

livro_s.criar_livro(session, 456, 'Contos Para Criancas', 'Vitor S Ferreira', 'Real', 2022)
livro_s.criar_livro(session, 457, 'As Lendas de Fogo e Gelo', 'Jorge Rodrigues', 'Leia', 2018)

exemplar_s.criar_exemplar(session, 111, 456)
exemplar_s.criar_exemplar(session, 112, 456)
exemplar_s.criar_exemplar(session, 113, 457)

emprestimo_s.criar_emprestimo(session, 1, 1234, '2025-10-06')
emprestimo_s.criar_emprestimo(session, 2, 1234, '2025-12-19')

emp_exemp_s.criar_emp_exemp(session, 111, 1)
emp_exemp_s.criar_emp_exemp(session, 113, 1)
emp_exemp_s.criar_emp_exemp(session, 112, 2)