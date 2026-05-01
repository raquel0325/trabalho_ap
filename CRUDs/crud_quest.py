import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connect import get_connection

class QuestionarioCRUD:
    #queestionario
    
    @staticmethod
    def inserir_resposta(id_funcionario, cidade, estado, formacao, curso, 
                        instituicao, ano_conclusao, ultimo_cargo, 
                        ultima_empresa, tempo_experiencia):
        #inserir resposta do questionário
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO respostas_questionario 
                (id_funcionario, cidade, estado, formacao, curso, instituicao, 
                 ano_conclusao, ultimo_cargo, ultima_empresa, tempo_experiencia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (id_funcionario, cidade, estado, formacao, curso, instituicao, 
                  ano_conclusao, ultimo_cargo, ultima_empresa, tempo_experiencia))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_funcionario(id_funcionario):
        #Busca o questionário de um funcionário
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM respostas_questionario 
                WHERE id_funcionario = ?
                ORDER BY data_preenchimento DESC
                LIMIT 1
            ''', (id_funcionario,))
            return cursor.fetchone()
        finally:
            conn.close()