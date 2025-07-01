# OBS: "#type: ignore" adicionado em alguns imports pois IDE (VSCode) nao
# entendia os import corretamente e acusava um "warning"
from sqlalchemy.orm import Session #type: ignore
from models.aluno import Aluno #type: ignore
from typing import List, Optional

# --- CREATE ---
def criar_aluno(session: Session, nome: str, matricula: int, email: str, curso: str) -> bool:
    # testa se ha um aluno ja cadastrado com uma matricula ou email no database
    teste_mat = session.get(Aluno, matricula)
    if teste_mat: # Se houver um aluno com matricula igual, abortar criacao
        print(f'\n***AVISO: ALUNO DE MATRICULA "{matricula}" JA EXISTENTE, ABORTANDO CRIACAO DE ALUNO\n')
        return False # erro
    
    teste_em = session.query(Aluno).filter(Aluno.email == email).all()
    if teste_em: # Se houver um aluno com email igual, abortar criacao
        print(f'\n***AVISO: ALUNO COM EMAIL "{email}" JA EXISTENTE, ABORTANDO CRIACAO DE ALUNO\n')
        return False # erro
    
    novo_aluno = Aluno(nome=nome, matricula=matricula, email=email, curso=curso)
    session.add(novo_aluno)
    session.commit()
    session.refresh(novo_aluno)
    
    print(f'\nAluno "{nome}", de matricula "{matricula}" criado\n')
    return True # tudo ok
    
# --- READ ---
def buscar_aluno_por_matricula(session: Session, matricula: int) -> Optional[Aluno]:
    # Obtem o aluno vinculado a essa matricula e o retorna
    return session.get(Aluno, matricula)

# diferente de buscar_aluno pois lista no console, enquanto buscar apenas obtem do banco de dados
def listar_aluno_por_matricula(session: Session, matricula: int) -> bool:
    aluno = buscar_aluno_por_matricula(session, matricula)
    if aluno:
        print(f'Aluno: {aluno.nome} --- Matricula: {aluno.matricula}')
        return True
    
    print(f'Aluno de matricula "{matricula}" nao encontrado!')
    return False

# diferente de listar_alunos pois apenas obtem a lista pelo query
def buscar_alunos(session: Session) -> List[Aluno]:
    # Executa uma consulta para buscar todos os registros da tabela Aluno
    return session.query(Aluno).all()

def listar_alunos(session: Session) -> bool:
    # Executa uma consulta para buscar todos os registros da tabela Aluno
    alunos = buscar_alunos(session)
    if alunos: # Se ha alunos, lista todos
        for aluno in alunos:
            print(f'Aluno: {aluno.nome} --- Matricula: {aluno.matricula}')
        return True # retorna tudo ok
    # Se nao tem alunos, retorna mensagem
    print('\nNenhum aluno encontrado!\n')
    return False # nada ok


# --- UPDATE ---
def atualizar_aluno(session: Session, matricula: int, nome: Optional[str] = None, email: Optional[str] = None, curso: Optional[str] = None) -> bool:
    # Busca o aluno que sera atualizado
    aluno_para_atualizar = buscar_aluno_por_matricula(session, matricula)
    
    # Se o aluno existir, atualiza seus campos
    if aluno_para_atualizar:
        # Confere se as informacoes estao vazias, soh atualiza as nao vazias
        print(f'\nIniciando a atualizacao da matricula "{matricula}"...')
        if nome is not None:
            aluno_para_atualizar.nome = nome
            #print(f'Mudando nome para {nome}...')  # saida de teste no console
        if email is not None:
            aluno_para_atualizar.email = email
            #print(f'Mudando email para {email}...')# saida de teste no console
        if curso is not None:
            aluno_para_atualizar.curso = curso
            #print(f'Mudando curso para {curso}...')# saida de teste no console
        
        # Confirma a transacao
        session.commit()
        print('Mudancas realizadas!\n')
        # Atualiza a instancia
        session.refresh(aluno_para_atualizar)
        return True # tudo ok
    
    # Se nao achou um aluno, retorna um erro
    print(f'\n***AVISO: ALUNO DE MATRICULA "{matricula}" NAO ENCONTRADO!\n')
    return False # erro encontrado

# --- DELETE ---
def remover_aluno(session: Session, matricula: int) -> bool:
    # Pega o aluno que sera deletado
    aluno_p_rem = buscar_aluno_por_matricula(session, matricula)
    
    # Se o aluno for encontrado, apaga ele do db
    if aluno_p_rem:
        session.delete(aluno_p_rem) # Marca para deletar
        session.commit() # Confirma a transacao
        print(f'\nAluno {aluno_p_rem.nome}, de matricula "{aluno_p_rem.matricula}" removido\n')
        return True # tudo ok
    # Se nao achar um aluno, avisa o usuario
    print(f'\n***AVISO: ALUNO DE MATRICULA "{matricula}" NAO ENCONTRADO!\n')
    return False # aluno nao encontrado
