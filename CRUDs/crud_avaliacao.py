import sqlite3
from config import Config
from database.connect import get_connection


class AvaliacaoCRUD: 
    @staticmethod
    def adicionar_avaliacao(id_freelancer, id_contratante, tipo_contratante, nota, comentario):
        """Adiciona ou atualiza uma avaliação para um freelancer"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # Verifica se já existe avaliação deste contratante
            print(tipo_contratante)
            print(id_contratante)
            print(id_freelancer)
            print(nota)
            print(comentario)
            cursor.execute("""
                SELECT id_avaliacao
                FROM avaliacoes
                WHERE id_freelancer = ?
                AND id_contratante = ?
                AND tipo_contratante = ?
            """, (id_freelancer, id_contratante, tipo_contratante))

            avaliacao_existente = cursor.fetchone()

            if avaliacao_existente:
                print("avaliacao existe")
            else:
                print(tipo_contratante)
                print(id_contratante)
                print(id_freelancer)
                print(nota)
                print(comentario)
                cursor.execute("""
                INSERT INTO avaliacoes (
                    id_freelancer,
                    id_contratante,
                    tipo_contratante,
                    nota, 
                    comentario
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                id_freelancer,
                id_contratante,
                tipo_contratante,
                nota,
                comentario
            ))

            # Atualiza total de avaliações do freelancer
            cursor.execute("""
                UPDATE freelancers
                SET total_avaliacoes = (
                    SELECT COUNT(*)
                    FROM avaliacoes
                    WHERE id_freelancer = ?
                )
                WHERE id_freelancer = ?
            """, (id_freelancer, id_freelancer))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("ERRO AO ADICIONAR AVALIAÇÃO")
            print(str(e))
            return False

        finally:
            conn.close()


    @staticmethod
    def calcular_media_avaliacoes(id_freelancer):
        """Calcula a média das avaliações de um freelancer"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT AVG(nota) as media, COUNT(*) as total
                FROM avaliacoes 
                WHERE id_freelancer = ?
            ''', (id_freelancer,))
            resultado = cursor.fetchone()
            
            if resultado and resultado['media']:
                return {
                    'media': round(resultado['media'], 1),
                    'total': resultado['total']
                }
            return {'media': 0, 'total': 0}
        finally:
            conn.close()
    
    @staticmethod
    def listar_avaliacoes_com_usuarios(id_freelancer):
        """Lista avaliações com dados do avaliador"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT *
            FROM avaliacoes
            WHERE id_freelancer = ?
            ORDER BY data_avaliacao DESC
        """, (id_freelancer,))
            avaliacoes = cursor.fetchall()

            resultado = []
            for av in avaliacoes:
                avaliacao = dict(av)

                if avaliacao['tipo_contratante'] == 'empresa':

                    cursor.execute("""
                        SELECT nome, email
                        FROM empresas
                        WHERE id_empresa = ?
                    """, (avaliacao['id_contratante'],))

                else:

                    cursor.execute("""
                        SELECT nome, email
                        FROM funcionarios
                        WHERE id_funcionario = ?
                    """, (avaliacao['id_contratante'],))

                usuario = cursor.fetchone()

                if usuario:
                    avaliacao['nome_avaliador'] = usuario['nome']
                    avaliacao['email_avaliador'] = usuario['email']
                else:
                    avaliacao['nome_avaliador'] = 'Usuário não encontrado'
                    avaliacao['email_avaliador'] = ''

                resultado.append(avaliacao)

            return resultado
      
        finally:
            conn.close()