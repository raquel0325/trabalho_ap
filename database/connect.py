import sqlite3

from config import Config # importa config para conexao, banco de dados e senha, etc 

def get_connection():
   #retorna uma conexão com o banco de dados
    conn = sqlite3.connect(Config.DB_PATH) # cria conexão
    conn.execute("PRAGMA foreign_keys = ON;") # ativa foreign keys
    conn.row_factory = sqlite3.Row  # retorna dicionário ao invés de tupla  
    return conn # retorna conexão

def get_cursor(): 
    """Retorna conexão e cursor já configurados"""
    conn = get_connection() # cria conexão
    return conn, conn.cursor() # retorna conexão e cursor