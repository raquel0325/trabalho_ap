from config import Config
import sqlite3
import os



def init_db():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    cursor.execute('''
    CREATE TABLE contratacoes (
        id_contratacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_freelancer INTEGER NOT NULL,
        id_funcionario INTEGER,
        id_empresa INTEGER,
        data_contratacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pendente'
        CHECK(status IN ('pendente','aceito','recusado','concluido','cancelado')),
        data_conclusao TIMESTAMP,
        FOREIGN KEY (id_freelancer) REFERENCES freelancers(id_freelancer) ON DELETE CASCADE,
        FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) ON DELETE CASCADE,
        FOREIGN KEY (id_empresa) REFERENCES empresas(id_empresa) ON DELETE CASCADE   )
    ''')
    

print('deu certo')