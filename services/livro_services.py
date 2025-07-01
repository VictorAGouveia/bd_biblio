# OBS: "#type: ignore" adicionado em alguns imports pois IDE (VSCode) nao
# entendia os import corretamente e acusava um "warning"
from sqlalchemy.orm import Session #type: ignore
from models.livro import Livro #type: ignore
from typing import List, Optional

# --- CREATE ---
def criar_livro(session: Session, codlivro: int, titulo: str, autor: str, editora: str, ano: int) -> bool:
    # testa se ha um aluno ja cadastrado com uma matricula ou email no database
    teste_cod = session.get(Livro, codlivro)
    if teste_cod: # Se houver um aluno com matricula igual, abortar criacao
        print(f'\n***AVISO: LIVRO DE CODIGO "{codlivro}" JA EXISTENTE, ABORTANDO CRIACAO DE LIVRO\n')
        return False # erro
    
    novo_livro = Livro(codlivro=codlivro, titulo=titulo, autor=autor, editora=editora, ano=ano)
    session.add(novo_livro)
    session.commit()
    session.refresh(novo_livro)
    
    print(f'\nLivro "{titulo}", de codigo "{codlivro}" criado\n')
    return True

# --- READ ---
def buscar_livro_por_codlivro(session: Session, codlivro: int) -> Optional[Livro]:
    return session.get(Livro, codlivro)

def listar_livro_por_codlivro(session: Session, codlivro: int) -> bool:
    livro = session.get(Livro, codlivro)
    if livro:
        print(f'{livro.titulo} - Por "{livro.autor}" ({livro.ano}) -- COD {livro.codlivro}')
        return True
    print(f'Livro de codigo {codlivro} nao encontrado!')
    return False

def buscar_livros(session: Session) -> List[Livro]:
    # Executa uma consulta para buscar todos os registros da tabela Livro
    return session.query(Livro).all()

def listar_livros(session: Session) -> bool:
    # Executa uma consulta para buscar todos os registros da tabela Livro
    livros = buscar_livros(session)
    if livros:
        for livro in livros:
            print(f'{livro.titulo} - Por "{livro.autor}" ({livro.ano}) -- COD {livro.codlivro}')
        return True
    print('Nenhum livro encontrado!')
    return False


# --- UPDATE ---
def atualizar_livro(session: Session, codlivro: int, titulo: Optional[str] = None, autor: Optional[str] = None, editora: Optional[str] = None, ano: Optional[int] = None) -> bool:
    # Busca o livro que sera atualizado
    livro_para_atualizar = buscar_livro_por_codlivro(session, codlivro)
    
    # Se o livro existir, atualiza seus campos
    if livro_para_atualizar:
        # Confere se as informacoes estao vazias, soh atualiza as nao vazias
        print(f'\nIniciando a atualizacao do livro de codigo "{codlivro}"...')
        if titulo is not None:
            livro_para_atualizar.titulo = titulo
            #print(f'Mudando titulo para {titulo}...')  # saida de teste no console
        if titulo is not None:
            livro_para_atualizar.autor = autor
            #print(f'Mudando titulo para {autor}...')   # saida de teste no console
        if editora is not None:
            livro_para_atualizar.editora = editora
            #print(f'Mudando editora para {editora}...')# saida de teste no console
        if ano is not None:
            livro_para_atualizar.ano = ano
            #print(f'Mudando editora para {ano}...')    # saida de teste no console
        
        # Confirma a transacao
        session.commit()
        print('Mudancas realizadas!\n')
        # Atualiza a instancia
        session.refresh(livro_para_atualizar)
        return True # tudo ok
    
    # Se nao achou um livro, retorna um erro
    print(f'\n***AVISO: LIRVO DE CODIGO "{codlivro}" NAO ENCONTRADO!\n')
    return False # erro encontrado

# --- DELETE ---
def remover_livro(session: Session, codlivro: int) -> bool:
    # Pega o livro que sera deletado
    livro_p_rem = buscar_livro_por_codlivro(session, codlivro)
    
    # Se o livro for encontrado, apaga ele do db
    if livro_p_rem:
        session.delete(livro_p_rem) # Marca para deletar
        session.commit() # Confirma a transacao
        print(f'\nLivro "{livro_p_rem.titulo}", de codigo "{livro_p_rem.codlivro}" removido\n')
        return True # tudo ok
    # Se nao achar um livro, avisa o usuario
    print(f'\n***AVISO: LIRVO DE CODIGO "{codlivro}" NAO ENCONTRADO!\n')
    return False # livro nao encontrado
