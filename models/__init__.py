from sqlalchemy.ext.declarative import declarative_base # type: ignore
# Usando o _init__ para criar uma base unificada para as classes, para corrigir
# problemas com referencias entre classes (como a matricula do emprestimo, que
# depende das matriculas de alunos)
Base = declarative_base()