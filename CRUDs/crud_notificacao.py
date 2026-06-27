from database.connect import get_connection


class NotificacaoCRUD:
    @staticmethod
    def inserir(id_usuario, titulo, mensagem, tipo, id_referencia: int | None = None):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO notificacoes (id_usuario, titulo, mensagem, tipo, id_referencia, lida)
                VALUES (?, ?, ?, ?, ?, 0)
                """,
                (id_usuario, titulo, mensagem, tipo, id_referencia),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def listar_por_usuario(id_usuario: int, apenas_nao_lidas: bool = False, limite: int = 20):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT id_notificacao, titulo, mensagem, tipo, id_referencia, lida, data_criacao
                FROM notificacoes
                WHERE id_usuario = ?
            """
            params = [id_usuario]

            if apenas_nao_lidas:
                query += " AND lida = 0"

            query += " ORDER BY data_criacao DESC LIMIT ?"
            params.append(limite)

            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()

    