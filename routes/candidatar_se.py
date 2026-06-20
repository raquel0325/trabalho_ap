from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Vaga, Candidatura, Match, Competencia  
from CRUDs import CandidaturaCRUD, MatchCRUD, CompetenciaCRUD  
from CRUDs.candidatura import CandidaturaCRUD

bp_candidatar_se = Blueprint('candidatar_se', __name__)




@bp_candidatar_se.route('/vaga/<int:id_vaga>', methods=['GET', 'POST'])
def detalhe_vaga(id_vaga):
    """Detalhes de uma vaga específica"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    vaga = Vaga.buscar(id_vaga)
    if not vaga:
        flash("Vaga não encontrada!", "erro")
        return redirect(url_for('vagas.listar_vagas'))
    
    id_funcionario = session['usuario_id']
    match_percent = Match.calcular(id_funcionario, id_vaga)
    match_degrees = match_percent * 3.6  
    
    ja_candidatou = CandidaturaCRUD.verificar_candidatura(id_funcionario, id_vaga)
    total_candidatos = CandidaturaCRUD.contar_candidatos_por_vaga(id_vaga)
    candidatos = CandidaturaCRUD.listar_candidatos_por_vaga(id_vaga)
    
    return render_template('vaga/vaga_detalhe.html', 
                         vaga=vaga, 
                         match_percent=match_percent,
                         match_degrees=match_degrees,
                         ja_candidatou=ja_candidatou,
                         total_candidatos=total_candidatos,
                         candidatos=candidatos)  

#======================================================================================================================================


#======================================================================================================================================


@bp_candidatar_se.route('/vaga/<int:id_vaga>/candidatar', methods=['POST'])
def candidatar_vaga(id_vaga):
    """Candidatar-se a uma vaga"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    try:
        Candidatura.candidatar(session['usuario_id'], id_vaga)
        flash('Candidatura realizada com sucesso!', 'sucesso')
    except ValueError as e:
        flash(str(e), 'erro')
    
    return redirect(url_for('candidatar_se.detalhe_vaga', id_vaga=id_vaga))

#======================================================================================================================================


#======================================================================================================================================
@bp_candidatar_se.route('/cancelar_candidatura/<int:id_candidatura>', methods=['POST'])
def cancelar_candidatura(id_candidatura):
    """Cancelar uma candidatura"""
    from CRUDs.candidatura import CandidaturaCRUD
    from database.connect import get_connection
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM candidaturas WHERE id_candidatura = ?', (id_candidatura,))
        conn.commit()
        conn.close()
        
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# ======================================================================================================================================


#======================================================================================================================================
@bp_candidatar_se.route('/candidatura/<int:id_candidatura>/status', methods=['POST'])
def alterar_status_candidatura(id_candidatura):
    """Altera o status de uma candidatura (empresa)"""
    if 'usuario_id' not in session or session.get('tipo') != 'empresa':
        flash('Não autorizado', 'erro')
        return redirect(url_for('vagas.listar_vagas'))
    
    try:
        novo_status = request.json.get('status')
        
        # Usa o model para atualizar (com validação)
        sucesso = Candidatura.atualizar_status(id_candidatura, novo_status)
        
        if sucesso:
            flash('Status da candidatura atualizado com sucesso!', 'sucesso')
            return redirect(url_for('vagas.listar_vagas'))
        else:
            flash('Candidatura não encontrada', 'erro')
            return redirect(url_for('vagas.listar_vagas'))
            
    except ValueError as e:
        flash(str(e), 'erro')
        return redirect(url_for('vagas.listar_vagas'))
    except Exception as e:
        flash('Ocorreu um erro ao atualizar o status da candidatura', 'erro')
        return redirect(url_for('vagas.listar_vagas'))

#======================================================================================================================================


#======================================================================================================================================
@bp_candidatar_se.route('/vaga/<int:id_vaga>/candidatos')
def ver_candidatos(id_vaga):
    """Página com lista de candidatos de uma vaga"""
    if 'usuario_id' not in session or session.get('tipo') != 'empresa':
        flash("Acesso não autorizado!", "erro")
        return redirect('/')
    
    vaga = Vaga.buscar(id_vaga)
    if not vaga:
        flash("Vaga não encontrada!", "erro")
        return redirect(url_for('vagas.empresa_vagas'))
    
    if vaga['id_empresa'] != session['usuario_id']:
        flash("Você não tem permissão para ver os candidatos desta vaga!", "erro")
        return redirect(url_for('vagas.empresa_vagas'))
    
    # Usa o model Candidatura
    total_candidatos = Candidatura.contar_por_vaga(id_vaga)
    candidatos = Candidatura.listar_candidatos_por_vaga(id_vaga)
    
    return render_template('home/ver_candidatos.html', 
                         vaga=vaga,
                         total_candidatos=total_candidatos,
                         candidatos=candidatos)