from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from models import Competencia, Questionario  
from database import get_connection  

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
#======================================================================================================================================

@bp_questionario.route('/salvar_questionario', methods=['POST'])
def salvar_questionario():

    id_func = request.form.get('id_func')

    # Verifica sessão
    if 'usuario_id' not in session or session['usuario_id'] != int(id_func):
        print("Sessão expirada. Faça login novamente!", "erro")
        return redirect('/')

    try:
        # Prepara os dados
        dados = {
            'cidade': request.form.get('cidade'),
            'estado': request.form.get('estado'),
            'formacao': request.form.get('formacao'),
            'curso': request.form.get('curso'),
            'instituicao': request.form.get('instituicao'),
            'ano_conclusao': request.form.get('ano_conclusao'),
            'ultimo_cargo': request.form.get('ultimo_cargo'),
            'ultima_empresa': request.form.get('ultima_empresa'),
            'tempo_experiencia': request.form.get('tempo_experiencia')
        }
        
        competencias_ids = request.form.getlist('competencias')
        novas_competencias = request.form.getlist('novas_competencias')
        
        # Salva usando o model
        Questionario.salvar(        
            id_funcionario=id_func,
            dados=dados,
            competencias_ids=competencias_ids,
            novas_competencias=novas_competencias
        )

        return redirect(url_for('home.home_pag'))
        
    except ValueError as e:
        flash(str(e), "erro")
    
    return redirect('/')