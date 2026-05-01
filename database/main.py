import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def init_db():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Tabela funcionarios
    cursor.execute('''CREATE TABLE IF NOT EXISTS funcionarios (
        id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT,
        email TEXT,
        senha TEXT,
        telefone TEXT,
        cpf TEXT NOT NULL UNIQUE    
    )''')
    
    # Tabela empresas
    cursor.execute('''CREATE TABLE IF NOT EXISTS empresas (
        id_empresa INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT,
        endereco TEXT,
        email TEXT,
        senha TEXT,
        telefone TEXT,
        cnpj TEXT NOT NULL UNIQUE
    )''')
    
    # Tabela competencias
    cursor.execute('''CREATE TABLE IF NOT EXISTS competencias (
        id_competencia INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT
    )''')
    
    # Tabela vagas
    cursor.execute('''CREATE TABLE IF NOT EXISTS vagas (
        id_vaga INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descricao TEXT,
        salario REAL,
        id_empresa INTEGER,
        id_competencia INTEGER,
        FOREIGN KEY (id_competencia) REFERENCES competencias (id_competencia),
        FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa)
    )''')
    
    # Tabela funcionario_competencias
    cursor.execute('''CREATE TABLE IF NOT EXISTS funcionario_competencias (
        id_funcionario INTEGER,
        id_competencia INTEGER,
        FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario),
        FOREIGN KEY (id_competencia) REFERENCES competencias (id_competencia)
    )''')
    
    # Tabela questionario
    cursor.execute('''CREATE TABLE IF NOT EXISTS respostas_questionario (
        id_resposta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_funcionario INTEGER,
        cidade TEXT,
        estado TEXT,
        formacao TEXT, 
        curso TEXT,
        instituicao TEXT,
        ano_conclusao INTEGER,
        ultimo_cargo TEXT,
        ultima_empresa TEXT,
        tempo_experiencia TEXT, 
        data_preenchimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario)
    )''')
    
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()