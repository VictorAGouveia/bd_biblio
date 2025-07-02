# Banco de Dados: Projeto 1

Este repositório possui o projeto da atividade de Banco de Dados, onde foi desenvolvido a base de um programa que atua sobre um banco de dados de uma biblioteca de uma universidade.

O servidor de banco de dados utilizado foi o PostgreSQL, sendo o programa desenvolvido em Python com auxilio da biblioteca SQLAlchemy e suas dependências.

## Estrutura dos arquivos

Os arquivos foram estruturados da seguinte forma:

- pasta `/models` - Contém as classes referentes às tabelas do banco de dados;
- pasta `/services` - Contém as definições das diversas operações sobre as tabelas;
- `db.py` - Responsável por definir a conexão com o banco de dados;
- `main.py` - Arquivo principal, contém o programa feito que testa todas as operações criadas;
- `criar_tabelas.py` - Arquivo que cria no banco de dados conectado as tabelas necessárias para o correto funcionamento de `main.py`, idealmente **deve ser executado antes de `main.py`**.

## Estrutura do BD

O banco de dados segue a estrutura definida pelo código SQL armazenado em `DEF_BD.sql`, note que **esse arquivo não cria nenhum objeto, apenas define as tabelas do banco de dados**.
