import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connect import get_connection
import sqlite3



class EmpresaCRUD:

    
    @staticmethod
    def inserir(nome, cnpj, email, senha, telefone='', endereco=''):
        """Insere uma nova empresa"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO empresas (nome, cnpj, email, senha, telefone, endereco) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, cnpj, email, senha, telefone, endereco))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise Exception("E-mail ou CNPJ já cadastrado!") from e
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_email_senha(email, senha):

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id_empresa, nome, email, cnpj 
                FROM empresas 
                WHERE email = ? AND senha = ?
            ''', (email, senha))
            return cursor.fetchone()
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_id(id_empresa):

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM empresas WHERE id_empresa = ?', 
                         (id_empresa,))
            return cursor.fetchone()
        finally:
            conn.close()
    @staticmethod
    def deletar(id_empresa):
        #deletar empresa
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM empresas WHERE id_empresa = ?', 
                         (id_empresa,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()