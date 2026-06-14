from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from models import Competencia, Questionario  # ← Importa do __init__.py
from database import get_connection  # ← Importa do __init__.py

bp_questionario = Blueprint('questionario', __name__)

@bp_questionario.route('/questionario/<int:id_func>')
def questionario_pag(id_func):
    if 'usuario_id' not in session or session['usuario_id'] != id_func:
        flash("Acesso não autorizado!", "erro")
        return redirect('/')
    
    competencias = Competencia.listar_todas()
    
    # Buscar cargos das vagas
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT titulo FROM vagas WHERE status = "ativa" ORDER BY titulo')
    cargos = cursor.fetchall()
    conn.close()
    
    return render_template('questionario.html', 
                         id_func=id_func, 
                         competencias=competencias,
                         cargos=cargos)