
import sqlite3
from database.connect import get_connection



class FuncionarioCRUD:
    
    @staticmethod
    def inserir(nome, email, senha, telefone, cpf):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO funcionarios (nome, email, senha, telefone, cpf) VALUES (?, ?, ?, ?, ?)''', 
                (nome, email, senha, telefone, cpf))
            conn.commit()
            return cursor.lastrowid
        except:
            raise Exception("E-mail ou CPF já cadastrado!")
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_email_senha(email, senha):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id_funcionario, nome, email, telefone, cpf FROM funcionarios WHERE email = ? AND senha = ?''', 
                (email, senha))
            return cursor.fetchone()
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_email(email):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id_funcionario, nome, email, telefone, cpf 
                FROM funcionarios 
                WHERE email = ?
            ''', (email,))
            return cursor.fetchone()
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_nome(nome):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM funcionarios WHERE nome = ?
            ''', (nome,))
            return cursor.fetchone()
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_id(id_funcionario):
        """Busca funcionário por ID e retorna como dicionário"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id_funcionario, nome, email, telefone, cpf 
                FROM funcionarios 
                WHERE id_funcionario = ?
            ''', (id_funcionario,))
            resultado = cursor.fetchone()
            if resultado:
                return dict(resultado)
            return None
        finally:
            conn.close()
    
    @staticmethod
    def atualizar(id_funcionario, nome=None, telefone=None, cpf=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            campos = []
            valores = []
            
            if nome:
                campos.append("nome = ?")
                valores.append(nome)
            if telefone:
                campos.append("telefone = ?")
                valores.append(telefone)
            if cpf:
                campos.append("cpf = ?")
                valores.append(cpf)
            
            if campos:
                valores.append(id_funcionario)
                cursor.execute(f'''
                    UPDATE funcionarios 
                    SET {', '.join(campos)}
                    WHERE id_funcionario = ?
                ''', valores)
                conn.commit()
                return True
            return False
        except sqlite3.IntegrityError:
            raise Exception("CPF já cadastrado!")
        finally:
            conn.close()
    
    
    @staticmethod
    def deletar(id_funcionario):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM funcionarios WHERE id_funcionario = ?', 
                         (id_funcionario,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
#======================================================================================================================================
