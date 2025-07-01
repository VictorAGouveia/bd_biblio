# OBS: "#type: ignore" adicionado em alguns imports pois IDE (VSCode) nao
# entendia os import corretamente e acusava um "warning"
from sqlalchemy.orm import Session #type: ignore
from models.emp_exemp import Emp_Exemp #type: ignore
from models.aluno import Aluno #type: ignore
from models.livro import Livro #type: ignore
from models.exemplar import Exemplar #type: ignore
from models.emprestimo import Emprestimo #type: ignore
from typing import List, Optional, Tuple

# --- CREATE ---
def criar_emp_exemp(session: Session, numtombo: int, codempres: int) -> bool:
    # testa se ha um aluno ja cadastrado com uma matricula ou email no database
    teste_em_ex = session.get(Emp_Exemp, numtombo)
    if teste_em_ex:
        print(f'***AVISO: EXEMPLAR DE TOMBO {numtombo} JA ESTA EM UMA RELACAO, ABORTANTO CRIACAO DE NOVA RELACAO')
        return False
    teste_exem = session.get(Exemplar, numtombo)
    teste_empr = session.get(Emprestimo, codempres)
    if teste_exem:
        if teste_empr: # Se houver um aluno com matricula igual, abortar criacao
            novo_emp_ex = Emp_Exemp(numtombo=numtombo, codempres=codempres)
            session.add(novo_emp_ex)
            session.commit()
            session.refresh(novo_emp_ex)
    
        print(f'\nExemplar de tombo "{numtombo}" relacionado com emprestimo "{codempres}"\n')
        return True
        
    print(f'\n***AVISO: EXEMPLAR DE TOMBO "{numtombo}" OU EMPRESTIMO "{codempres}" NAO ENCONTRADO, ABORTANDO CRIACAO DE RELACAO\n')
    return False # erro
    
# --- READ ---
def buscar_emp_exemp_por_numtombo(session: Session, numtombo: int) -> Optional[Emp_Exemp]:
    return session.get(Emp_Exemp, numtombo)

def listar_emp_exemp_por_numtombo(session: Session, numtombo: int) -> Optional[Emp_Exemp]:
    emp_exemp = buscar_emp_exemp_por_numtombo(session, numtombo)
    if emp_exemp:
        exemp = session.get(Exemplar, emp_exemp.numtombo)
        empres = session.get(Emprestimo, emp_exemp.codempres)
        livro = session.get(Livro, exemp.codlivro)
        aluno = session.get(Aluno, empres.matricula)
        print(f'Exemplar No {exemp.numtombo} do Livro "{livro.titulo}" -> Emprestimo {empres.codempres} do(a) aluno(a) {aluno.nome}')
        return True
    print('Nenhuma relacao encontrada!')
    return False

def buscar_emp_exemp(session: Session) -> List[Emp_Exemp]:
    # Executa uma consulta para buscar todos os registros da tabela Exemplar
    return session.query(Emp_Exemp).all()

# Essa funcao serve para fazer um query conjunto, que vai obter todos os livros
# e alunos relacionados com uma tabela emp_exemp, feita em uma funcao separada
# pois eh util caso se queira usa-la fora dos services
def consulta_completa(session: Session) -> Tuple[List[Emp_Exemp], List[Aluno], List[Livro]]:

    consulta_completa = session.query(
        Emp_Exemp,
        Aluno,
        Livro
    ).select_from(Emp_Exemp).join(
            Emprestimo, Emp_Exemp.codempres == Emprestimo.codempres
    ).join(
        Aluno, Emprestimo.matricula == Aluno.matricula
    ).join(
        Exemplar, Emp_Exemp.numtombo == Exemplar.numtombo
    ).join(
        Livro, Exemplar.codlivro == Livro.codlivro
    ).order_by(Emp_Exemp.codempres)

    if consulta_completa:
        return consulta_completa
    print('Nenhuma relacao obtida!')
    return None

def listar_emp_exemp(session: Session) -> bool:
    # Executa uma consulta para buscar todos os registros da tabela Exemplar
    cons_comp = consulta_completa(session)

    emp_at = -1
    for emp_ex, aluno, livro in cons_comp.all():
        if(emp_ex.codempres != emp_at):
            print(f'\nEmprestimo {emp_ex.codempres} - Aluno: {aluno.nome}')
            emp_at = emp_ex.codempres
        print(f' | Livro: {livro.titulo} (Exemplar de Tombo {emp_ex.numtombo})')

# *** NAO HA NECESSIDADE DE ATUALIZAR A RELACAO EMP_EXEMP
# Se houver um exemplar a ser realocado, ele antes deve ser desligado de uma relacao
# para que possa ser relacionado novamente, mas como eu desenvolvi isso no automatico
# deixo abaixo por referencia
"""def atualizar_emp_exemp(session: Session, numtombo: int, codempres = int) -> bool:
    # Busca o exemp que sera atualizado
    relacao_para_atualizar = buscar_emp_exemp_por_numtombo(session, numtombo)
    
    # Se o a relacao existir, atualiza seus campos
    if relacao_para_atualizar:
        # Confere se as informacoes estao vazias, soh atualiza as nao vazias
        print(f'\nIniciando a atualizacao do exemp de codigo "{numtombo}"...')
        if codempres is not None:
            teste_emp = session.get(Emprestimo, codempres)
            if teste_emp:
                relacao_para_atualizar.codempres = codempres
                print(f'Mudando emprestimo para codigo "{codempres}"...')
            else:
                print(f'\n***AVISO: EMPRESTIMO "{codempres}" NAO ENCONTRADO, ABORTANDO ALTERACAO DO EMPRESTIMO\n')

        # Confirma a transacao
        session.commit()
        print('Mudancas realizadas!\n')
        # Atualiza a instancia
        session.refresh(relacao_para_atualizar)
        return True # tudo ok
    
    # Se nao achou um exemp, retorna um erro
    print(f'\n***AVISO: RELACAO DO TOMBO "{numtombo}" NAO ENCONTRADA!\n')
    return False # erro encontrado"""

# --- DELETE ---
def remover_emp_exemp(session: Session, numtombo: int) -> bool:
    # Pega o exemp que sera deletado
    emp_ex_p_rem = buscar_emp_exemp_por_numtombo(session, numtombo)
    
    # Se o exemp for encontrado, apaga ele do db
    if emp_ex_p_rem:
        session.delete(emp_ex_p_rem) # Marca para deletar
        session.commit() # Confirma a transacao
        print(f'\nRelacao do tombo "{emp_ex_p_rem.numtombo}" com emprestimo "{emp_ex_p_rem.codempres}" removido\n')
        return True # tudo ok
    # Se nao achar um exemp, avisa o usuario
    print(f'\n***AVISO: RELACAO DO TOMBO "{numtombo}" NAO ENCONTRADA!\n')
    return False # exemp nao encontrado
