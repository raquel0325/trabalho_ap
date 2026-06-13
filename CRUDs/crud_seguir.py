import sys
import os
from database.connect import get_connection

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SeguirCRUD:
    @staticmethod
    def listar_outros_usuarios(id_usuario_atual):
        """Lista todos os funcionários exceto o atual (para a seção Pessoas)"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id_funcionario, nome, email 
                FROM funcionarios 
                WHERE id_funcionario != ?
                ORDER BY nome
            ''', (id_usuario_atual,))
            return cursor.fetchall()
        finally:
            conn.close()
    @staticmethod
    def seguir(seguidor_id, seguido_id):
        """Registra que um usuário segue outro"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO seguidores (seguidor_id, seguido_id)
                VALUES (?, ?)
            ''', (seguidor_id, seguido_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    @staticmethod
    def deixar_seguir(seguidor_id, seguido_id):
        """Remove o seguimento entre usuários"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM seguidores 
                WHERE seguidor_id = ? AND seguido_id = ?
            ''', (seguidor_id, seguido_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    @staticmethod
    def verificar_seguindo(seguidor_id, seguido_id):
        """Verifica se um usuário segue outro"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM seguidores 
                WHERE seguidor_id = ? AND seguido_id = ?
            ''', (seguidor_id, seguido_id))
            return cursor.fetchone() is not None
        finally:
            conn.close()
    
    @staticmethod
    def listar_seguidores(usuario_id):
        """Lista todos os seguidores de um usuário"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.id_funcionario, f.nome, f.email
                FROM seguidores s
                JOIN funcionarios f ON s.seguidor_id = f.id_funcionario
                WHERE s.seguido_id = ?
                ORDER BY f.nome
            ''', (usuario_id,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def listar_seguindo(usuario_id):
        """Lista todos os usuários que um usuário segue"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.id_funcionario, f.nome, f.email
                FROM seguidores s
                JOIN funcionarios f ON s.seguido_id = f.id_funcionario
                WHERE s.seguidor_id = ?
                ORDER BY f.nome
            ''', (usuario_id,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def contar_seguidores(usuario_id):
        """Conta quantos seguidores um usuário tem"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) as total FROM seguidores WHERE seguido_id = ?
            ''', (usuario_id,))
            resultado = cursor.fetchone()
            return resultado['total'] if resultado else 0
        finally:
            conn.close()
    
    @staticmethod
    def contar_seguindo(usuario_id):
        """Conta quantos usuários um usuário segue"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) as total FROM seguidores WHERE seguidor_id = ?
            ''', (usuario_id,))
            resultado = cursor.fetchone()
            return resultado['total'] if resultado else 0
        finally:
            conn.close()