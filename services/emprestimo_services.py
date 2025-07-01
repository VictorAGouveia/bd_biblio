# OBS: "#type: ignore" adicionado em alguns imports pois IDE (VSCode) nao
# entendia os import corretamente e acusava um "warning"
from sqlalchemy.orm import Session #type: ignore
from models.emprestimo import Emprestimo #type: ignore
from models.aluno import Aluno #type: ignore
from typing import List, Optional

from datetime import datetime, timedelta # usado para calcular as operacoes com datas

# --- CREATE ---
# Nao cria com data de devolucao e atraso, pois supoe-se que se cria o emprestimo na hora que ele eh feito
def criar_emprestimo(session: Session, codempres: int, matricula: int, data_emp: str) -> bool:
    # testa se ha um emprestimo ja cadastrado com uma codempres ou email no database
    teste_cod = session.get(Emprestimo, codempres)
    if teste_cod: # Se houver um emprestimo com codempres igual, abortar criacao
        print(f'\n***AVISO: EMPRESTIMO DE CODIGO "{codempres}" JA EXISTENTE, ABORTANDO CRIACAO DE EMPRESTIMO\n')
        return False # erro
    
    teste_mat = session.get(Aluno, matricula)
    
    if teste_mat:
        _data_emp = datetime.strptime(data_emp, '%Y-%m-%d') # transforma em datetime, para facilitar operacoes

        emp_diff = timedelta(days=7) # a previsao da entrega eh 7 dias apos a entrega
        data_prev = datetime.strftime(_data_emp + emp_diff, '%Y-%m-%d') # cria a data prevista em string
    
        novo_emprestimo = Emprestimo(codempres=codempres, matricula=matricula, data_emp=data_emp, data_prev=data_prev)
        session.add(novo_emprestimo)
        session.commit()
        session.refresh(novo_emprestimo)
    
        print(f'\nEmprestimo para matricula "{matricula}", de codempres "{codempres}" criado\n')
        return True # tudo ok
    
    print(f'\n***AVISO: ALUNO DE MATRICULA "{matricula}" NAO ENCONTRADO, ABORTANDO CRIACAO DO EMPRESTIMO\n')
    

# --- READ ---
def buscar_emprestimo_por_codempres(session: Session, codempres: int) -> Optional[Emprestimo]:
    return session.get(Emprestimo, codempres)

def listar_emprestimo_por_codempres(session: Session, codempres: int) -> bool:
    empres = session.get(Emprestimo, codempres)
    if empres:
        aluno = session.get(Aluno, empres.matricula)
        print(f'-- Emprestimo {empres.codempres}, feito por "{aluno.nome}".\nData: {empres.data_emp} -->> Prev: {empres.data_prev}')
        return True
    print(f'Emprestimo {codempres} nao encontrado!')
    return False

def buscar_emprestimos(session: Session) -> List[Emprestimo]:
    # Executa uma consulta para buscar todos os registros da tabela Emprestimo
    return session.query(Emprestimo).all()

def listar_emprestimos(session: Session) -> bool:
    # Executa uma consulta para buscar todos os registros da tabela Emprestimo
    empress = buscar_emprestimos(session)
    if empress:
        matriculas = {emprestimo.matricula for emprestimo in empress}
        alunos = session.query(Aluno).filter(Aluno.matricula.in_(matriculas)).all()
        alunos_mat = {aluno.matricula: aluno for aluno in alunos}
        for empres in empress:
            _aluno = alunos_mat.get(empres.matricula)
            print(f'-- Emprestimo {empres.codempres}, feito por "{_aluno.nome}".')
            if empres.data_dev:
                print(f'Data: {empres.data_emp} -->> Dev: {empres.data_dev}')
                if empres.atraso > 0:
                    print(f'!! Atraso de {empres.atraso} dias !!')
            else:
                print(f'Data: {empres.data_emp} -->> Prev: {empres.data_prev}')
            print('--------------------')
        return True
    print('Emprestimos nao encontrados!')
    return False

# --- UPDATE ---
def atualizar_emprestimo(session: Session, codempres: int, 
                         matricula: Optional[int], data_emp: Optional[str],
                         data_dev: Optional[str]) -> bool:
    # Busca o emprestimo que sera atualizado
    emprestimo_para_atualizar = buscar_emprestimo_por_codempres(session, codempres)
    
    # Se o emprestimo existir, atualiza seus campos
    if emprestimo_para_atualizar:
        # Confere se as informacoes estao vazias, soh atualiza as nao vazias
        print(f'\nIniciando a atualizacao do emprestimo "{codempres}"...')
        if matricula is not None:
            teste_mat = session.get(Aluno, matricula)
            if teste_mat:
                emprestimo_para_atualizar.matricula = matricula
                #print(f'Mudando matricula para {matricula}...')    # saida de teste no console 
            else:
                print(f'\n***AVISO: ALUNO DE MATRICULA "{matricula}" NAO ENCONTRADO, ABORTANDO ALTERACAO DA MATRICULA\n')
        if data_emp is not None:
            emprestimo_para_atualizar.data_emp = data_emp
            #print(f'Mudando data do emprestimo para {data_emp}...')    # saida de teste no console 

            _data_emp = datetime.strptime(data_emp, '%Y-%m-%d') # transforma em datetime, para facilitar operacoes

            emp_diff = timedelta(days=7) # a previsao da entrega eh 7 dias apos a entrega
            data_prev = datetime.strftime(_data_emp + emp_diff, '%Y-%m-%d') # cria a data prevista em string
            
            emprestimo_para_atualizar.data_prev = data_prev
            #print(f'Mudando data prevista para {data_prev}...')        # saida de teste no console 

        if data_dev is not None:
            emprestimo_para_atualizar.data_dev = data_dev
            #print(f'Mudando data de devolucao para {data_dev}...')     # saida de teste no console 

            # converte das datas de devolucao e previstas para calculo do atraso
            _data_dev = datetime.strptime(data_dev, '%Y-%m-%d')
            _data_prev = datetime.strptime(emprestimo_para_atualizar.data_prev, '%Y-%m-%d')

            atraso = (_data_dev - _data_prev).days
            if atraso < 0: atraso = 0

            emprestimo_para_atualizar.atraso = atraso
            #print(f'Mudando atraso de devolucao para {atraso} dias...')# saida de teste no console 


        # Confirma a transacao
        session.commit()
        print('Mudancas realizadas!\n')
        # Atualiza a instancia
        session.refresh(emprestimo_para_atualizar)
        return True # tudo ok
    
    # Se nao achou um emprestimo, retorna um erro
    print(f'\n***AVISO: EMPRESTIMO DE CODIGO "{codempres}" NAO ENCONTRADO!\n')
    return False # erro encontrado

# --- DELETE ---
def remover_emprestimo(session: Session, codempres: int) -> bool:
    # Pega o emprestimo que sera deletado
    emprestimo_p_rem = buscar_emprestimo_por_codempres(session, codempres)
    
    # Se o emprestimo for encontrado, apaga ele do db
    if emprestimo_p_rem:
        session.delete(emprestimo_p_rem) # Marca para deletar
        session.commit() # Confirma a transacao
        print(f'\nEmprestimo para matricula "{emprestimo_p_rem.matricula}", de codempres "{emprestimo_p_rem.codempres}" removido\n')
        return True # tudo ok
    # Se nao achar um emprestimo, avisa o usuario
    print(f'\n***AVISO: EMPRESTIMO DE CODIGO "{codempres}" NAO ENCONTRADO!\n')
    return False # emprestimo nao encontrado
