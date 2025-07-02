create TABLE Livro(
    CodLivro INTEGER,
    Editora VARCHAR(48) NOT NULL,
    Autor VARCHAR(48) NOT NULL,
    Titulo VARCHAR(48) NOT NULL,
    Ano INTEGER NOT NULL,
    PRIMARY KEY(CodLivro)
);
  
create TABLE Aluno(
    Matricula INTEGER,
    Nome VARCHAR(48) NOT NULL,
    Email VARCHAR(48) NOT NULL,
    Curso VARCHAR(48) NOT NULL,
    PRIMARY KEY(Matricula),
    UNIQUE(Email)
);
  
create TABLE Emprestimo(
    CodEmpres INTEGER,
    Matricula INTEGER,
    Data_emp DATE NOT NULL,
    Data_prev DATE NOT NULL,
    Data_dev DATE,
    Atraso INTEGER,
    PRIMARY KEY(CodEmpres),
    FOREIGN key(Matricula) REFERENCES Aluno(Matricula)
);
  
create TABLE Exemplar(
    NumTombo INTEGER,
    CodLivro INTEGER,
    PRIMARY KEY(NumTombo),
    FOREIGN key(CodLivro) REFERENCES Livro(CodLivro)
);
  
create TABLE Emp_Exemp(
    NumTombo INTEGER,
    CodEmpres INTEGER,
    PRIMARY KEY(NumTombo),
    FOREIGN key(CodEmpres) REFERENCES Emprestimo(CodEmpres),
    FOREIGN key(NumTombo) REFERENCES Exemplar(NumTombo)
);
