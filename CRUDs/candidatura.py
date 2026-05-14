import sys
import os
import sqlite3
from database.connect import get_connection

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connect import get_connection


class CandidaturaCRUD:
    """CRUD para operações com candidaturas"""
    
    @staticmethod
    def candidatar(id_funcionario, id_vaga):
        """Registra candidatura de um funcionário a uma vaga"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO candidaturas (id_funcionario, id_vaga, data_candidatura)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (id_funcionario, id_vaga))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    @staticmethod
    def listar_candidaturas_funcionario(id_funcionario):
        """Lista candidaturas de um funcionário"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, v.titulo, v.descricao, v.salario, e.nome as empresa_nome,
                       c.data_candidatura
                FROM candidaturas c
                JOIN vagas v ON c.id_vaga = v.id_vaga
                JOIN empresas e ON v.id_empresa = e.id_empresa
                WHERE c.id_funcionario = ?
                ORDER BY c.data_candidatura DESC
            ''', (id_funcionario,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def listar_candidatos_vaga(id_vaga):
        """Lista candidatos de uma vaga com match score"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.id_funcionario, f.nome, f.email, f.telefone,
                       c.data_candidatura,
                       rq.formacao, rq.ultimo_cargo, rq.tempo_experiencia
                FROM candidaturas c
                JOIN funcionarios f ON c.id_funcionario = f.id_funcionario
                LEFT JOIN respostas_questionario rq ON f.id_funcionario = rq.id_funcionario
                WHERE c.id_vaga = ?
                ORDER BY c.data_candidatura DESC
            ''', (id_vaga,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def verificar_candidatura(id_funcionario, id_vaga):
        """Verifica se funcionário já se candidatou"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM candidaturas 
                WHERE id_funcionario = ? AND id_vaga = ?
            ''', (id_funcionario, id_vaga))
            return cursor.fetchone() is not None
        finally:
            conn.close()


class MatchCRUD:
    
    @staticmethod
    def calcular(id_funcionario, id_vaga):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) as total FROM vaga_competencias WHERE id_vaga = ?', (id_vaga,))
            total_vaga = cursor.fetchone()['total']
            
            if total_vaga == 0:
                return 0
            
            cursor.execute('''
                SELECT COUNT(*) as match 
                FROM funcionario_competencias 
                WHERE id_funcionario = ? 
                AND id_competencia IN (SELECT id_competencia FROM vaga_competencias WHERE id_vaga = ?)
            ''', (id_funcionario, id_vaga))
            
            match = cursor.fetchone()['match']
            return round((match / total_vaga) * 100)
        finally:
            conn.close()
    
    @staticmethod
    def listar_melhores(id_funcionario, limite=20):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT v.*, e.nome as empresa_nome
                FROM vagas v
                JOIN empresas e ON v.id_empresa = e.id_empresa
                ORDER BY v.id_vaga DESC
            ''')
            vagas = cursor.fetchall()
            
            resultado = []
            for vaga in vagas:
                match = MatchCRUD.calcular(id_funcionario, vaga['id_vaga'])
                if match > 0:
                    vaga_dict = dict(vaga)
                    vaga_dict['match_percent'] = match
                    resultado.append(vaga_dict)
            
            resultado.sort(key=lambda x: x['match_percent'], reverse=True)
            return resultado[:limite]
        finally:
            conn.close()