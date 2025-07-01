# OBS: "#type: ignore" adicionado em alguns imports pois IDE (VSCode) nao
# entendia os import corretamente e acusava um "warning"
from sqlalchemy.orm import Session #type: ignore
from models.exemplar import Exemplar #type: ignore
from models.livro import Livro #type: ignore
from models.emp_exemp import Emp_Exemp #type: ignore
from typing import List, Optional

# --- CREATE ---
def criar_exemplar(session: Session, numtombo: int, codlivro: int) -> bool:
    # testa se ha um aluno ja cadastrado com uma matricula ou email no database
    teste_tom = session.get(Exemplar, numtombo)
    if teste_tom: # Se houver um aluno com matricula igual, abortar criacao
        print(f'\n***AVISO: EXEMPLAR DE TOMBO "{numtombo}" JA EXISTENTE, ABORTANDO CRIACAO DE EXEMPLAR\n')
        return False # erro
    
    teste_liv = session.get(Livro, codlivro)
    if teste_liv:
        novo_exemplar = Exemplar(numtombo=numtombo, codlivro=codlivro)
        session.add(novo_exemplar)
        session.commit()
        session.refresh(novo_exemplar)
    
        print(f'\nExemplar de tombo "{numtombo}", do livro "{codlivro}" criado\n')
        return True
    
    print(f'\n***AVISO: LIVRO DE CODIGO "{codlivro}" NAO ENCONTRADO, ABORTANDO CRIACAO DO EXEMPLAR\n')


def buscar_exemplar_por_numtombo(session: Session, numtombo: int) -> Optional[Exemplar]:
    return session.get(Exemplar, numtombo)

def listar_exemplar_por_numtombo(session: Session, numtombo: int) -> bool:
    exemp = buscar_exemplar_por_numtombo(session, numtombo)
    if exemp:
        livro = session.get(Livro, exemp.codlivro)
        print(f'Exemplar No {exemp.numtombo} - Livro: {livro.titulo}')
        return True
    print(f'Exemplar nao encontrado!')
    return False

# --- READ ---
def buscar_exemplares(session: Session) -> List[Exemplar]:
    # Executa uma consulta para buscar todos os registros da tabela Exemplar
    return session.query(Exemplar).all()

def listar_exemplares(session: Session) -> List[Exemplar]:
    # Executa uma consulta para buscar todos os registros da tabela Exemplar
    exemps = buscar_exemplares(session)
    if exemps:
        codlivros = {exemplar.codlivro for exemplar in exemps}
        livros = session.query(Livro).filter(Livro.codlivro.in_(codlivros)).all()
        livros_cod = {livro.codlivro: livro for livro in livros}
        for exemp in exemps:
            _livro = livros_cod.get(exemp.codlivro)
            print(f'Exemplar No {exemp.numtombo} - Livro: {_livro.titulo}')
        return True
    print('Nenhum exemplar encontrado!')
    return False

# --- UPDATE ---
def atualizar_exemplar(session: Session, numtombo: int, codlivro = int) -> bool:
    # Busca o exemp que sera atualizado
    exemplar_para_atualizar = buscar_exemplar_por_numtombo(session, numtombo)
    
    # Se o exemp existir, atualiza seus campos
    if exemplar_para_atualizar:
        # Confere se as informacoes estao vazias, soh atualiza as nao vazias
        print(f'\nIniciando a atualizacao do exemp de codigo "{numtombo}"...')
        if codlivro is not None:
            teste_liv = session.get(Livro, codlivro)
            if teste_liv:
                exemplar_para_atualizar.codlivro = codlivro
                print(f'Mudando codigo do livro para {codlivro}...')
            else:
                print(f'\n***AVISO: LIVRO DE CODIGO "{codlivro}" NAO ENCONTRADO, ABORTANDO ALTERACAO DO LIVRO\n')

        # Confirma a transacao
        session.commit()
        print('Mudancas realizadas!\n')
        # Atualiza a instancia
        session.refresh(exemplar_para_atualizar)
        return True # tudo ok
    
    # Se nao achou um exemp, retorna um erro
    print(f'\n***AVISO: EXEMPLAR DE TOMBO "{numtombo}" NAO ENCONTRADO!\n')
    return False # erro encontrado

# --- DELETE ---
def remover_exemplar(session: Session, numtombo: int) -> bool:
    # testa se o exemplar nao esta com uma relacao definida, a relacao deve ser removida antes
    teste_rel = session.get(Emp_Exemp, numtombo)
    if teste_rel:
        print(f'***AVISO: O EXEMPLAR {numtombo} POSSUI UMA RELACAO COM O EMPRESTIMO {teste_rel.codempres}, REMOVA A RELACAO ANTES')
    
    # Pega o exemp que sera deletado
    exemp_p_rem = buscar_exemplar_por_numtombo(session, numtombo)
    
    # Se o exemp for encontrado, apaga ele do db
    if exemp_p_rem:
        session.delete(exemp_p_rem) # Marca para deletar
        session.commit() # Confirma a transacao
        print(f'\nExemplar {exemp_p_rem.numtombo}, do livro "{exemp_p_rem.codlivro}" removido\n')
        return True # tudo ok
    # Se nao achar um exemp, avisa o usuario
    print(f'\n***AVISO: EXEMPLAR DE TOMBO "{numtombo}" NAO ENCONTRADO!\n')
    return False # exemp nao encontrado
