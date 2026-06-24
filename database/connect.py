import sqlite3

from config import Config

def get_connection():
    """Retorna uma conexão com o banco de dados"""
    conn = sqlite3.connect(Config.DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row  
    return conn

def get_cursor():
    """Retorna conexão e cursor já configurados"""
    conn = get_connection()
    return conn, conn.cursor()