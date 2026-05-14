from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.model_vagas import Vaga, Candidatura, Match
from CRUDs.candidatura import CandidaturaCRUD, MatchCRUD
from models.model_comp import Competencia


bp_vagas = Blueprint('vagas', __name__)

@bp_vagas.route('/vagas')
def listar_vagas():
    if 'usuario_id' not in session :
        return redirect('/')
    
    busca = request.args.get('busca', '')
    salario_min = request.args.get('salario_min', '')
    empresa = request.args.get('empresa', '')
    
    salario_min_float = float(salario_min) if salario_min else None
    
    vagas = Vaga.listar_todas(
        busca=busca if busca else None,
        salario_min=salario_min_float,
        empresa=empresa if empresa else None
    )
    
    id_funcionario = session['usuario_id']
    from CRUDs.candidatura import CandidaturaCRUD
    
    vagas_formatadas = []
    for vaga in vagas:
        vaga_dict = dict(vaga) 
        vaga_dict['match_percent'] = Match.calcular(id_funcionario, vaga_dict['id_vaga'])
        vaga_dict['candidatou'] = CandidaturaCRUD.verificar_candidatura(id_funcionario, vaga_dict['id_vaga'])
        vagas_formatadas.append(vaga_dict)

    return render_template('vaga/vagas_listar.html', vagas=vagas_formatadas)
    


@bp_vagas.route('/empresa/vaga/criar', methods=['GET', 'POST'])
def empresa_criar_vaga():
    if 'usuario_id' not in session or session.get('tipo') != 'empresa':
        return redirect('/')
    
    if request.method == 'GET':
        return render_template('home/criar_vaga.html', 
                             competencias=Competencia.listar_todas())
    
    try:
        id_vaga = Vaga.criar(
            titulo=request.form.get('titulo'),
            descricao=request.form.get('descricao'),
            salario=float(request.form.get('salario')) if request.form.get('salario') else None,
            cidade=request.form.get('cidade'),
            regime=request.form.get('regime'),  
            id_empresa=session['usuario_id'],
            competencias_ids=request.form.getlist('competencias')
        )
        flash("Vaga criada com sucesso!", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro: {str(e)}", "erro")
    
    return redirect(url_for('vagas.empresa_vagas'))

@bp_vagas.route('/empresa/vagas')
def empresa_vagas():
    """Exibe as vagas cadastradas pela empresa logada"""
    if 'usuario_id' not in session or session.get('tipo') != 'empresa':
        return redirect('/')
    
    from models.model_vagas import Vaga
    vagas = Vaga.listar_empresa(session['usuario_id'])
    
    return render_template('home/home_emp.html', vagas=vagas)

@bp_vagas.route('/vaga/<int:id_vaga>/candidatar', methods=['POST'])
def candidatar_vaga(id_vaga):
    """Candidatar-se a uma vaga"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    try:
        Candidatura.candidatar(session['usuario_id'], id_vaga)
        flash('Candidatura realizada com sucesso!', 'sucesso')
    except ValueError as e:
        flash(str(e), 'erro')
    
    return redirect(url_for('vagas.detalhe_vaga', id_vaga=id_vaga))

@bp_vagas.route('/vaga/<int:id_vaga>')
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
    
    from CRUDs.candidatura import CandidaturaCRUD
    ja_candidatou = CandidaturaCRUD.verificar_candidatura(id_funcionario, id_vaga)
    
    return render_template('vaga/vaga_detalhe.html', 
                         vaga=vaga, 
                         match_percent=match_percent,
                         match_degrees=match_degrees,
                         ja_candidatou=ja_candidatou)
