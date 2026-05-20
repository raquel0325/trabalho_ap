from flask import Blueprint, render_template, request
import sys
import os
import sqlite3
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connect import get_connection

def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

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

@app.route('/publicar-vaga', methods=['GET', 'POST'])
def publicar_vaga():
    if request.method == 'POST':
        # Captura os dados do formulário
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        salario = request.form['salario']
        cidade = request.form['cidade']
        regime = request.form['regime']
        
        # Validação básica
        if not all([titulo, descricao, salario, cidade, regime]):
            flash('Todos os campos são obrigatórios!', 'error')
            return render_template('publicar_vaga.html')
        
        try:
            # Converte salário para float
            salario = float(salario.replace(',', '.'))
            
            # Conecta ao banco e insere os dados
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Por enquanto, usando valores padrão para id_empresa e id_competencia
            # Você pode ajustar isso conforme sua lógica de negócio
            cursor.execute('''
                INSERT INTO vagas (titulo, descricao, salario, cidade, regime, id_empresa, id_competencia)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (titulo, descricao, salario, cidade, regime, 1, 1))
            
            conn.commit()
            conn.close()
            
            flash('Vaga publicada com sucesso!', 'success')
            return redirect(url_for('listar_vagas'))  # Redireciona para página de vagas
            
        except ValueError:
            flash('Salário inválido! Use apenas números.', 'error')
            return render_template('publicar_vaga.html')
        except Exception as e:
            flash(f'Erro ao publicar vaga: {str(e)}', 'error')
            return render_template('publicar_vaga.html')
    
    # Se for GET, apenas mostra o formulário
    return render_template('publicar_vaga.html')
