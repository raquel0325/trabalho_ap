from flask import Blueprint, render_template, request
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connect import get_connection

bp_vagas = Blueprint('vagas', __name__)

@bp_vagas.route('/vagas', methods=['GET'])
def listar_vagas():
    """Lista vagas com filtros"""
    conn = get_connection()
    cursor = conn.cursor()
    
    termo_busca = request.args.get('busca', '')
    salario = request.args.get('salario', '')
    
    cursor.execute("""
        SELECT v.*, e.nome as empresa_nome, c.nome as competencia_nome
        FROM vagas v
        LEFT JOIN empresas e ON v.id_empresa = e.id_empresa
        LEFT JOIN competencias c ON v.id_competencia = c.id_competencia
        WHERE v.titulo LIKE ? 
    """, (f'%{termo_busca}%',))
    
    vagas = cursor.fetchall()
    conn.close()
    
    return render_template('listar_vagas.html', vagas=vagas)