from CRUDs.crud_comp import CompetenciaCRUD
from database.connect import get_connection
class Competencia:
    """Classe que contém as regras de negócio para competências"""
    
    @staticmethod
    def listar_todas():
        """Lista todas as competências disponíveis"""
        return CompetenciaCRUD.listar_todas()
    
    @staticmethod
    def adicionar_ao_funcionario(id_funcionario, competencia):
        """
        Adiciona uma competência ao funcionário.
        
        Args:
            id_funcionario: ID do funcionário
            competencia: Pode ser:
                - int: ID da competência existente
                - str: Nome da competência (será criada se não existir)
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Verifica se é ID ou nome
            if isinstance(competencia, int):
                # É um ID - verifica se existe
                cursor.execute('SELECT id_competencia, nome FROM competencias WHERE id_competencia = ?', (competencia,))
                resultado = cursor.fetchone()
                if not resultado:
                    raise ValueError(f"Competência com ID {competencia} não encontrada")
                id_competencia = resultado[0]
            else:
                # É um nome - busca ou cria
                nome_comp = competencia.strip()
                cursor.execute('SELECT id_competencia FROM competencias WHERE nome = ?', (nome_comp,))
                resultado = cursor.fetchone()
                
                if resultado:
                    id_competencia = resultado[0]
                else:
                    # Cria nova competência
                    cursor.execute('INSERT INTO competencias (nome) VALUES (?)', (nome_comp,))
                    conn.commit()
                    id_competencia = cursor.lastrowid
            
            # Vincula ao funcionário (evita duplicidade)
            cursor.execute('''
                INSERT OR IGNORE INTO funcionario_competencias (id_funcionario, id_competencia)
                VALUES (?, ?)
            ''', (id_funcionario, id_competencia))
            conn.commit()
            return id_competencia
        finally:
            conn.close()
    
    @staticmethod
    def listar_do_funcionario(id_funcionario):
        """Lista competências de um funcionário"""
        return CompetenciaCRUD.listar_do_funcionario(id_funcionario)