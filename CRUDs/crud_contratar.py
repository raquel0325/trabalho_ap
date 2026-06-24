import sqlite3
from config import Config
from database.connect import get_connection

class ContratacaoCRUD:
    @staticmethod
    def contratar_freelancer(id_freelancer, id_contratante):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO contratacoes (
                    id_freelancer,
                    id_contratante,
                    status
                )
                VALUES (?, ?, 'aceito')
            """, (id_freelancer, id_contratante))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print(e)
            return False

        finally:
            conn.close()
# =================================================================================================================
    @staticmethod
    def listar_contratacao(id_contratante):
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute("""SELECT
                        c.id_contratacao,
                        c.data_contratacao,
                        c.status,
                        f.id_freelancer,
                        f.profissao,
                        f.servico_oferecido,
                        f.preco_medio,
                        fu.nome AS nome_freelancer
                    FROM contratacoes c
                    INNER JOIN freelancers f
                    ON c.id_freelancer = f.id_freelancer
                INNER JOIN funcionarios fu
                    ON f.id_funcionario = fu.id_funcionario
                WHERE c.id_contratante = ?
                ORDER BY c.data_contratacao DESC
            """, (id_contratante,))

            return cursor.fetchall()

        finally:
            conn.close()
#=================================================================================================================
    @staticmethod
    def buscar_por_id(id_contratacao):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM contratacoes WHERE id_contratacao = ?
            ''', (id_contratacao,))
            return cursor.fetchone()
        finally:
            conn.close()
#=================================================================================================================
    @staticmethod
    def buscar_por_funcionario(id_funcionario):
        """Busca contratação por ID do funcionário (freelancer)"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.* FROM contratacoes c
                INNER JOIN freelancers f ON c.id_freelancer = f.id_freelancer
                WHERE f.id_funcionario = ?
            ''', (id_funcionario,))
            return cursor.fetchone()
        finally:
            conn.close()
#=================================================================================================================
    @staticmethod
    def listar_contratados(id_contratante):
        """Lista freelancers contratados por um contratante"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, f.profissao, f.servico_oferecido, f.preco_medio,
                       func.nome as nome_freelancer
                FROM contratacoes c
                INNER JOIN freelancers f ON c.id_freelancer = f.id_freelancer
                INNER JOIN funcionarios func ON f.id_funcionario = func.id_funcionario
                WHERE c.id_contratante = ? AND c.status != 'cancelado'
                ORDER BY c.data_contratacao DESC
            ''', (id_contratante,))
            return cursor.fetchall()
        finally:
            conn.close()


    @staticmethod
    def buscar_por_freelancer_e_contratante(id_freelancer, id_contratante):
        """Verifica se existe uma contratação entre freelancer e contratante"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM contratacoes 
                WHERE id_freelancer = ? AND id_contratante = ? 
                AND status IN ('aceito', 'concluido')
            ''', (id_freelancer, id_contratante))
            return cursor.fetchone()
        finally:
            conn.close()