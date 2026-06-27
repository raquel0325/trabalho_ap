import sqlite3
from config import Config
from database.connect import get_connection

class ContratacaoCRUD:
    @staticmethod
    def contratar_freelancer(id_freelancer, id_contratante, tipo_contratante):
        conn = get_connection()
        print(id_freelancer)
        print(id_contratante)
        print(tipo_contratante)
        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO contratacoes (
                    id_freelancer,
                    id_contratante,
                    tipo_contratante,
                    status
                )
                VALUES (?, ?, ?, 'pendente')
            """, (id_freelancer, id_contratante, tipo_contratante))

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
    def buscar_por_freelancer_e_contratante(id_freelancer, id_contratante,tipo_contratante):
        """Verifica se existe uma contratação entre freelancer e contratante"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM contratacoes 
                WHERE id_freelancer = ? AND id_contratante = ? AND tipo_contratante =?
                AND status IN ('pendente','aceito','recusado','concluido','cancelado')
            ''', (id_freelancer, id_contratante,tipo_contratante))
            return cursor.fetchone()
        finally:
            conn.close()
#=================================================================================================================
    @staticmethod
    def listar_solicitantes(id_freelancer):
        """
        Lista todos que solicitaram um freelancer específico,
        trazendo nome e e-mail do solicitante independente de ser
        funcionario ou empresa.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT
                    c.id_contratacao,
                    c.id_contratante,
                    c.tipo_contratante,
                    c.status,
                    c.data_contratacao
                FROM contratacoes c
                WHERE c.id_freelancer = ?
                ORDER BY c.data_contratacao DESC
            ''', (id_freelancer,))
            rows = cursor.fetchall()
 
            resultado = []
            for row in rows:
                item = dict(row)
 
                # Busca nome/email do contratante conforme o tipo
                if item['tipo_contratante'] == 'empresa':
                    cursor.execute('''
                        SELECT nome, email,telefone FROM empresas WHERE id_empresa = ?
                    ''', (item['id_contratante'],))
                else:
                    cursor.execute('''
                        SELECT nome, email,telefone FROM funcionarios WHERE id_funcionario = ?
                    ''', (item['id_contratante'],))
 
                contratante = cursor.fetchone()
                if contratante:
                    item['nome_contratante'] = contratante['nome']
                    item['email_contratante'] = contratante['email']
                    item['telefone_contratante'] = contratante['telefone']
                else:
                    item['nome_contratante'] = 'Desconhecido'
                    item['email_contratante'] = ''
                    item['telefone_contratante'] = ''
    
                resultado.append(item)
 
            return resultado
        finally:
            conn.close()
 
    # =================================================================================================================
    # NOVO: atualiza o status de uma contratação (usado pelo freelancer)
    @staticmethod
    def atualizar_status(id_contratacao, novo_status, id_freelancer_dono):
        """
        Atualiza o status de uma contratação.        Statuses válidos: pendente, aceito, recusado, concluido, cancelado
        """
        statuses_validos = {'pendente', 'aceito', 'recusado', 'concluido', 'cancelado'}
        if novo_status not in statuses_validos:
            return False
 
        conn = get_connection()
        try:
            cursor = conn.cursor()
 
            # Verifica se a contratação pertence a um freelancer do funcionário logado
            cursor.execute('''
                SELECT c.id_contratacao
                FROM contratacoes c
                INNER JOIN freelancers f ON c.id_freelancer = f.id_freelancer
                WHERE c.id_contratacao = ?
                  AND f.id_funcionario = ?
            ''', (id_contratacao, id_freelancer_dono))
 
            if not cursor.fetchone():
                return False  # Não é dono, nega
 
            # Se concluído, salva a data
            if novo_status == 'concluido':
                cursor.execute('''
                    UPDATE contratacoes
                    SET status = ?, data_conclusao = CURRENT_TIMESTAMP
                    WHERE id_contratacao = ?
                ''', (novo_status, id_contratacao))
            else:
                cursor.execute('''
                    UPDATE contratacoes
                    SET status = ?
                    WHERE id_contratacao = ?
                ''', (novo_status, id_contratacao))
 
            conn.commit()
            return cursor.rowcount > 0
 
        except Exception as e:
            conn.rollback()
            print("Erro ao atualizar status:", e)
            return False
        finally:
            conn.close()
