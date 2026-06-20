from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.connect import get_connection
from models import Vaga, Candidatura, Match, Competencia  
from CRUDs import CandidaturaCRUD, MatchCRUD, CompetenciaCRUD, VagaCRUD


bp_atualizar_vaga = Blueprint('atualizar_vaga', __name__)

@bp_atualizar_vaga.route('/vaga/<int:id_vaga>/editar', methods=['GET', 'POST'])
def editar_vaga(id_vaga):
    """Editar uma vaga específica"""
    if 'usuario_id' not in session or session.get('tipo') != 'empresa':
        return redirect('/')
    vaga = Vaga.buscar(id_vaga)
    if not vaga:
        return redirect(url_for('vagas.listar_vagas'))
    if vaga['id_empresa'] != session['usuario_id']:
        return redirect(url_for('vagas.empresa_vagas'))
    if request.method == 'GET':
        competencias = CompetenciaCRUD.listar_todas()
        competencias_vaga = VagaCRUD.buscar_competencias_vaga(id_vaga) # busca as competências associadas à vaga       
        competencias_ids_vaga = [comp['id_competencia'] for comp in competencias_vaga] # extrai os IDs das competências associadas à vaga e os salva no array
        
        return render_template('home/editar_vaga.html', 
                             vaga=vaga,
                             competencias=competencias,
                             competencias_ids_vaga=competencias_ids_vaga)
    try:
        # Atualiza dados na tabela vagas
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        salario = float(request.form.get('salario')) if request.form.get('salario') else None
        cidade = request.form.get('cidade')
        regime = request.form.get('regime')
        competencias_ids = request.form.getlist('competencias')

        # atualiza os dados 
        VagaCRUD.atualizar(id_vaga, titulo, descricao, salario, cidade, regime)

        # remove competencias antigas
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM vaga_competencias WHERE id_vaga = ?', (id_vaga,))
        #adiciona a nova lista de competencias
        for comp_id in competencias_ids:
            if comp_id:
                cursor.execute('INSERT INTO vaga_competencias (id_vaga, id_competencia) VALUES (?, ?)',
                             (id_vaga, comp_id))
        
        conn.commit()
        conn.close()
        flash("Vaga atualizada com sucesso!", "sucesso")
        
    except Exception as e:
        flash(f"Erro ao atualizar: {str(e)}", "erro")
    
    return redirect(url_for('vagas.empresa_vagas'))
#======================================================================================================================================