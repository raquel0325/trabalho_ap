
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
#======================================================================================================================================
    @staticmethod
    def atualizar(id_funcionario, cidade=None, estado=None, formacao=None, curso=None, 
                instituicao=None, ultimo_cargo=None, ultima_empresa=None, 
                tempo_experiencia=None, ano_conclusao=None):
        """Atualiza os dados do questionário de um funcionário"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE respostas_questionario 
                SET cidade = ?, estado = ?, formacao = ?, curso = ?, 
                    instituicao = ?, ultimo_cargo = ?, ultima_empresa = ?, 
                    tempo_experiencia = ?, ano_conclusao = ?, data_preenchimento = CURRENT_TIMESTAMP
                WHERE id_funcionario = ?
            ''', (
                cidade,
                estado,
                formacao,
                curso,
                instituicao,
                ultimo_cargo,
                ultima_empresa,
                tempo_experiencia,
                ano_conclusao,
                id_funcionario
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()