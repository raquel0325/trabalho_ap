import sqlite3
from config import Config
from database.connect import get_connection


class FreelancerCRUD:

    @staticmethod
    def inserir(profissao, servico_oferecido, preco_medio, disponibilidade, id_funcionario):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO freelancers (
                    id_funcionario,
                    profissao,
                    servico_oferecido,
                    preco_medio,
                    disponibilidade,
                    total_avaliacoes
                )
                VALUES (?, ?, ?, ?, ?, 0)
            ''', (
                id_funcionario,
                profissao,
                servico_oferecido,
                preco_medio,
                disponibilidade
            ))
            #print("INSERT executado")
            conn.commit()

            return cursor.lastrowid

        except sqlite3.IntegrityError as e:
            print("IntegrityError:", e)
            raise Exception(f"IntegrityError: {e}")

        except Exception as e:
            print("Erro geral:", e)
            raise

        finally:
            conn.close()
#=================================================================================================================
    @staticmethod
    def buscar_freelancer(filtros=None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = '''
                SELECT * FROM freelancers
                WHERE 1=1
            '''
            params = []
            
            if filtros:
                if filtros.get('busca'):
                    query += " AND (profissao LIKE ? OR servico_oferecido LIKE ?)"
                    params.extend([f"%{filtros['busca']}%", f"%{filtros['busca']}%"])
                
                if filtros.get('disponibilidade'):
                    query += " AND disponibilidade = ?"
                    params.append(filtros['disponibilidade'])
                
                if filtros.get('preco_medio_min') is not None:
                    query += " AND preco_medio >= ?"
                    params.append(filtros['preco_medio_min'])
                
                if filtros.get('preco_medio_max') is not None:
                    query += " AND preco_medio <= ?"
                    params.append(filtros['preco_medio_max'])
            
            query += " ORDER BY preco_medio DESC"
            
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()

#=================================================================================================================
    @staticmethod
    def listar_por_funcionario(id_funcionario):
        """Lista todos os freelances de um funcionário"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM freelancers 
                WHERE id_funcionario = ?
                ORDER BY data_cadastro DESC
            ''', (id_funcionario,))
            return cursor.fetchall()
        finally:
            conn.close()
#=================================================================================================================
    @staticmethod
    def buscar_por_funcionario(id_funcionario):
        """Busca um freelance pelo ID do funcionário"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM freelancers WHERE id_funcionario = ?
            ''', (id_funcionario,))
            return cursor.fetchone()
        finally:
            conn.close()
#=================================================================================================================
    @staticmethod
    def buscar_por_id(id_freelancer):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM freelancers WHERE id_freelancer = ?
            ''', (id_freelancer,))
            return cursor.fetchone()
        finally:
            conn.close()
#=================================================================================================================        
    @staticmethod
    def listar_todas():
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM freelancers
            ''')
            return cursor.fetchall()
        finally:
            conn.close()
#=================================================================================================================
    @staticmethod
    def atualizar_status(id_freelancer, status):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE freelancers SET disponibilidade = ? WHERE id_freelancer = ?
            ''', (status, id_freelancer))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
#=================================================================================================================
