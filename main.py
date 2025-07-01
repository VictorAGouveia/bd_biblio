from db import SessionLocal
from models.aluno import Aluno
from models.livro import Livro
from models.emprestimo import Emprestimo
from models.exemplar import Exemplar
from models.emp_exemp import Emp_Exemp
import services.aluno_services as aluno_s
import services.livro_services as livro_s
import services.emprestimo_services as emprestimo_s
import services.exemplar_services as exemplar_s
import services.emp_exemp_services as emp_exemp_s

session = SessionLocal()

# --- Testes do CRUD p/ Aluno ---
#""" <<< Descomente isso para desativar essa sessao do codigo
print('\n----------------------------------------\n--- TESTES PARA OPERACOES DOS ALUNOS ---\n----------------------------------------\n')
# garantindo que matricula 1236 estara livre, provavelmente resultara em erro
aluno_s.remover_aluno(session, 1236)

# Leitura
aluno_s.listar_alunos(session)

# cria aluno na matricula 1236
aluno_s.criar_aluno(session, 'Armando B', 1236, 'armando@hotmail.com', 'Geologia')

# lista o aluno 1236
aluno_s.listar_aluno_por_matricula(session, 1236)

# tenta criar um aluno de novo em 1236, edve resultar em erro
aluno_s.criar_aluno(session, 'Arlindo B', 1236, 'arlindo@hotmail.com', 'Geografia')

# atualiza o aluno 1236
aluno_s.atualizar_aluno(session, 1236, 'Arlindo B', 'arlindo@hotmail.com', 'Geografia')

# lista todos os alunos presentes
aluno_s.listar_alunos(session)

# remove aluno 1236
aluno_s.remover_aluno(session, 1236)
#"""

# --- Testes do CRUD p/ Livro ---
#""" <<< Descomente isso para desativar essa sessao do codigo
print('\n----------------------------------------\n--- TESTES PARA OPERACOES DOS LIVROS ---\n----------------------------------------\n')

# garante que codigo 458 estara livre, provavelmente da erro
livro_s.remover_livro(session, 458)

# lista todos os livros presentes
livro_s.listar_livros(session)

# cria livro com codigo 458
livro_s.criar_livro(session, 458, 'Uma grande storia', 'Frederico', 'Sariava', 2022)

# lista apenas o livro 458
livro_s.listar_livro_por_codlivro(session, 458)

# tenta criar um livro em cima de 458, deve dar erro
livro_s.criar_livro(session, 458, 'Uma Grande Historia', 'Fredericson', 'Sairava', 2022)

# atualiza o livro 458
livro_s.atualizar_livro(session, 458, 'Uma Grande Historia', 'Fredericson', 'Sairava')

# lista todos os livros
livro_s.listar_livros(session)

# remove livro 458
livro_s.remover_livro(session, 458)
#"""

# --- Testes do CRUD p/ Emprestimo ---
#""" <<< Descomente isso para desativar essa sessao do codigo
print('\n---------------------------------------------\n--- TESTES PARA OPERACOES DOS EMPRESTIMOS ---\n---------------------------------------------\n')
# garante que emprestimo 123 estara livre, provavelmente resultara em erro
emprestimo_s.remover_emprestimo(session, 123)

# lista todos os emprestimos presentes
emprestimo_s.listar_emprestimos(session)

# cria emprestimo com codigo 123 
emprestimo_s.criar_emprestimo(session, 123, 1234, '2025-12-06')

# lista apenas o emprestimo 123
emprestimo_s.listar_emprestimo_por_codempres(session, 123)

# tenta criar um emprestimo em cima de 123, deve dar erro
emprestimo_s.criar_emprestimo(session, 123, 1235, '2025-14-06')

# atualiza o emprestimo 123
emprestimo_s.atualizar_emprestimo(session, 123, 1240, '2025-06-12', '2025-07-21')

# lista todos os emprestimos
emprestimo_s.listar_emprestimos(session)

# remove emprestimo 123
emprestimo_s.remover_emprestimo(session, 123)
#"""

# --- Testes do CRUD p/ Exemplar ---
#""" <<< Descomente isso para desativar essa sessao do codigo
print('\n--------------------------------------------\n--- TESTES PARA OPERACOES DOS EXEMPLARES ---\n--------------------------------------------\n')
# garante que o tombo 123 estara livre, provavelmente resultara em erro
exemplar_s.remover_exemplar(session, 123)

# lista todos os exemplares presentes
exemplar_s.listar_exemplares(session)

# cria exemplar 123 do livro 456
exemplar_s.criar_exemplar(session, 123, 456)

# lista apenas exemplar 123
exemplar_s.listar_exemplar_por_numtombo(session, 123)

# tenta criar em cima do exemplar 123, deve dar erro
exemplar_s.criar_exemplar(session, 123, 457)

# atualiza o exemplar 123 para o livro 457
exemplar_s.atualizar_exemplar(session, 123, 457)

# lista todos os exemplares
exemplar_s.listar_exemplares(session)

# remove o exemplar 123
exemplar_s.remover_exemplar(session, 123)
#"""

# --- Testes do CRUD p/ Emp_Exemp ---
#""" <<< Descomente isso para desativar essa sessao do codigo
print('\n------------------------------------------------------------------------\n--- TESTES PARA OPERACOES DA TABELA RELACIONAL EMPRESTIMO-EXEMPLARES ---\n------------------------------------------------------------------------\n')

# cria emprestimo 321 e exemplar 123 para uso durante testes
emprestimo_s.criar_emprestimo(session, 321, 1234, '2025-12-06')
exemplar_s.criar_exemplar(session, 123, 456)

# libera a relacao do tombo 123, "um emprestimo pode ter varios livros, mas um livro so pode estar em um emprestimo"
emp_exemp_s.remover_emp_exemp(session, 123)

# lista todos os emprestimos
emp_exemp_s.listar_emp_exemp(session)

# cria a relacao do exemplar 123 com o emprestimo 321
emp_exemp_s.criar_emp_exemp(session, 123, 321)

# lista a relacao recem criada
emp_exemp_s.listar_emp_exemp_por_numtombo(session, 123)

# tenta criar uma relacao em cima do exemplar 123, deve retornar erro
emp_exemp_s.criar_emp_exemp(session, 123, 1)

# cria mais dois livros, um emprestimo e duas relacoes para testar listagem de mais de uma relacao
emprestimo_s.criar_emprestimo(session, 231, 1235, '2025-12-06')
exemplar_s.criar_exemplar(session, 124, 456)
exemplar_s.criar_exemplar(session, 125, 457)

emp_exemp_s.criar_emp_exemp(session, 124, 321)
emp_exemp_s.criar_emp_exemp(session, 125, 231)

# lista todos os exemplares
emp_exemp_s.listar_emp_exemp(session)

# apaga todos os relacionamentos, exemplares e emprestimos criados
# apaga relacoes
emp_exemp_s.remover_emp_exemp(session, 123)
emp_exemp_s.remover_emp_exemp(session, 124)
emp_exemp_s.remover_emp_exemp(session, 125)
# apaga emoprestimos
emprestimo_s.remover_emprestimo(session, 321)
emprestimo_s.remover_emprestimo(session, 231)
# apaga exemplares
exemplar_s.remover_exemplar(session, 123)
exemplar_s.remover_exemplar(session, 124)
exemplar_s.remover_exemplar(session, 125)

#"""