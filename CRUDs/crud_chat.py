import sqlite3
from config import Config
from database.connect import get_connection


class ChatCRUD:
    @staticmethod
    def abrir_sala(id_candidatura):
        """Cria a sala de chat para uma candidatura (se não existir)"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO salas_chat (id_candidatura) VALUES (?)', (id_candidatura,))
            conn.commit()
            id_sala = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Se já existir, apenas busca o ID dela
            cursor.execute('SELECT id_sala FROM salas_chat WHERE id_candidatura = ?', (id_candidatura,))
            id_sala = cursor.fetchone()[0]
        finally:
            conn.close()
        return id_sala

    @staticmethod
    def buscar_sala_por_candidatura(id_candidatura):
        """Busca o ID da sala usando a candidatura"""
        conn =  get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id_sala FROM salas_chat WHERE id_candidatura = ?', (id_candidatura,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None

    @staticmethod
    def inserir_mensagem(id_sala, id_remetente, tipo_remetente, mensagem):
        """Salva a mensagem no banco"""
        conn =  get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mensagens_chat (id_sala, id_remetente, tipo_remetente, mensagem)
            VALUES (?, ?, ?, ?)
        ''', (id_sala, id_remetente, tipo_remetente, mensagem))
        conn.commit()
        id_msg = cursor.lastrowid
        conn.close()
        return id_msg

    @staticmethod
    def listar_mensagens(id_sala):
        """Puxa o histórico de mensagens"""
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id_mensagem, id_remetente, tipo_remetente, mensagem, enviado_em 
            FROM mensagens_chat 
            WHERE id_sala = ? ORDER BY enviado_em ASC
        ''', (id_sala,))
        mensagens = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return mensagens