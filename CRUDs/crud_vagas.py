
import sys
import os
import sqlite3
from database.connect import get_connection

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class VagaCRUD:
    
    @staticmethod
    def inserir(titulo, descricao, salario,cidade, regime, id_empresa, competencias_ids):
        """Insere uma nova vaga e vincula competências"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Insere a vaga
            cursor.execute('''
                INSERT INTO vagas (titulo, descricao, salario, cidade, regime, id_empresa) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (titulo, descricao, salario, cidade, regime, id_empresa))
            
            id_vaga = cursor.lastrowid
            
            # Vincula competências à vaga
            for id_competencia in competencias_ids:
                cursor.execute('''
                    INSERT INTO vaga_competencias (id_vaga, id_competencia)
                    VALUES (?, ?)
                ''', (id_vaga, id_competencia))
            
            conn.commit()
            return id_vaga
        finally:
            conn.close()
    
#'''========================================================================='''
    
    @staticmethod
    def listar_por_empresa(id_empresa):
        """Lista todas as vagas de uma empresa"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Passo 1: Buscar todas as vagas da empresa
            cursor.execute('''
                SELECT * FROM vagas WHERE id_empresa = ? ORDER BY id_vaga DESC''',(id_empresa,))
            vagas = cursor.fetchall()
            
            return vagas
            
        finally:
            conn.close()
    
#'''========================================================================='''

    
    @staticmethod
    def buscar_por_id(id_vaga):
        """Busca uma vaga pelo ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT v.*, e.nome as empresa_nome
                FROM vagas v
                JOIN empresas e ON v.id_empresa = e.id_empresa
                WHERE v.id_vaga = ?
            ''', (id_vaga,))
            return cursor.fetchone()
        finally:
            conn.close()

#'''========================================================================='''

    @staticmethod
    def buscar_competencias_vaga(id_vaga):
        """Busca competências de uma vaga"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id_competencia, c.nome
                FROM vaga_competencias vc
                JOIN competencias c ON vc.id_competencia = c.id_competencia
                WHERE vc.id_vaga = ?
            ''', (id_vaga,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    @staticmethod
    def atualizar(id_vaga, titulo=None, descricao=None, salario=None, cidade=None, regime=None):
        """Atualiza dados de uma vaga"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            campos = []
            valores = []
            
            if titulo:
                campos.append("titulo = ?")
                valores.append(titulo)
            if descricao:
                campos.append("descricao = ?")
                valores.append(descricao)
            if salario is not None:
                campos.append("salario = ?")
                valores.append(salario)
            if cidade:
                campos.append("cidade = ?")
                valores.append(cidade)
            if regime:
                campos.append("regime = ?")
                valores.append(regime)

            if campos:
                valores.append(id_vaga)
                cursor.execute(f'''
                    UPDATE vagas 
                    SET {', '.join(campos)}
                    WHERE id_vaga = ?
                ''', valores)
                conn.commit()
                return True
            return False
        finally:
            conn.close()


#'''========================================================================='''

    @staticmethod
    def deletar(id_vaga):
        """Remove uma vaga"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Remove vínculos com competências
            cursor.execute('DELETE FROM vaga_competencias WHERE id_vaga = ?', (id_vaga,))
            
            # Remove candidaturas
            cursor.execute('DELETE FROM candidaturas WHERE id_vaga = ?', (id_vaga,))
            
            # Remove a vaga
            cursor.execute('DELETE FROM vagas WHERE id_vaga = ?', (id_vaga,))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()


#'''========================================================================='''


    @staticmethod
    def listar_todas(filtros=None):
        """Lista todas as vagas com filtros"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            query = '''
                SELECT v.*, e.nome as empresa_nome,
                       GROUP_CONCAT(DISTINCT c.nome) as competencias 
                FROM vagas v
                JOIN empresas e ON v.id_empresa = e.id_empresa 
                LEFT JOIN vaga_competencias vc ON v.id_vaga = vc.id_vaga
                LEFT JOIN competencias c ON vc.id_competencia = c.id_competencia 
                WHERE 1=1
            '''
            params = []
            
            if filtros:
                if filtros.get('busca'):
                    query += " AND (v.titulo LIKE ? OR v.descricao LIKE ?)"
                    params.extend([f"%{filtros['busca']}%", f"%{filtros['busca']}%"])
                
                if filtros.get('salario_min'):
                    query += " AND v.salario >= ?"
                    params.append(filtros['salario_min'])
                
                if filtros.get('empresa'):
                    query += " AND e.nome LIKE ?"
                    params.append(f"%{filtros['empresa']}%")
            
            query += " GROUP BY v.id_vaga ORDER BY v.id_vaga DESC"
            
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()
