import sys
import os
from database.connect import get_connection
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CompetenciaCRUD:
    #competencias
    
    @staticmethod
    def listar_todas():

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM competencias ORDER BY nome")
            return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_nome(nome):

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM competencias WHERE nome = ?", (nome,))
            return cursor.fetchone()
        finally:
            conn.close()
    
    @staticmethod
    def inserir(nome):

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO competencias (nome) VALUES (?)", (nome,))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Se já existe, retorna o ID
            return CompetenciaCRUD.buscar_por_nome(nome)['id_competencia']
        finally:
            conn.close()
    
    @staticmethod
    def vincular_funcionario(id_funcionario, id_competencia):

        conn = get_connection()
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO funcionario_competencias 
                (id_funcionario, id_competencia) 
                VALUES (?, ?)
            ''', (id_funcionario, id_competencia))
            conn.commit()
            return True
        finally:
            conn.close()
    
    @staticmethod
    def listar_do_funcionario(id_funcionario):

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.* 
                FROM competencias c
                JOIN funcionario_competencias fc ON c.id_competencia = fc.id_competencia
                WHERE fc.id_funcionario = ?
                ORDER BY c.nome
            ''', (id_funcionario,))
            return cursor.fetchall()
        finally:
            conn.close()