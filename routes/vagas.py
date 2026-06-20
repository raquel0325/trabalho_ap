from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Vaga, Candidatura, Match, Competencia  
from CRUDs import CandidaturaCRUD, MatchCRUD, CompetenciaCRUD, VagaCRUD  

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
#======================================================================================================================================


#======================================================================================================================================
    


@bp_vagas.route('/empresa/vaga/criar', methods=['GET', 'POST'])
def empresa_criar_vaga():
    if 'usuario_id' not in session or session.get('tipo') != 'empresa':
        return redirect('/')
    
    if request.method == 'GET':
        from database.connect import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT titulo FROM vagas WHERE titulo IS NOT NULL ORDER BY titulo")
        titulos = cursor.fetchall()
        conn.close()
        return render_template('home/criar_vaga.html', 
                             competencias=Competencia.listar_todas(),
                             titulos=titulos
                             )          
            
    
    try:
        competencias_ids = request.form.getlist('competencias')
        
        novas_competencias = request.form.getlist('competencias_novas_marcadas')
        
        print(f"IDs existentes (devem ser números): {competencias_ids}")
        print(f"Nomes das novas (devem ser textos): {novas_competencias}")
        
        for nome_comp in novas_competencias:
            nome_comp = nome_comp.strip()
            if nome_comp:
                existente = CompetenciaCRUD.buscar_por_nome(nome_comp)
                
                if existente:
                    if isinstance(existente, dict):
                        comp_id = existente['id_competencia']
                    else:
                        comp_id = existente[0]
                    print(f"Competência '{nome_comp}' já existe com ID {comp_id}")
                else:
                    comp_id = CompetenciaCRUD.inserir(nome_comp)
                    print(f"Competência '{nome_comp}' foi criada com ID {comp_id}")
                
                competencias_ids.append(str(comp_id))
        
        competencias_ids = list(set(competencias_ids))
        
        print(f"Lista final de IDs: {competencias_ids}")
        
        # Validação
        if not competencias_ids:
            raise ValueError("Selecione pelo menos uma competência!")
        
        cidade = request.form.get('cidade') or request.form.get('endereco') or 'Não informada'
        


        id_vaga = Vaga.criar(
            titulo=request.form.get('titulo'),
            descricao=request.form.get('descricao'),
            salario=float(request.form.get('salario')) if request.form.get('salario') else None,
            cidade=cidade,
            regime=request.form.get('regime'),  
            id_empresa=session['usuario_id'],
            competencias_ids= competencias_ids
        )
        flash("Vaga criada com sucesso!", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro: {str(e)}", "erro")
    
    return redirect(url_for('vagas.empresa_vagas'))
#======================================================================================================================================


#======================================================================================================================================
@bp_vagas.route('/empresa/vagas')
def empresa_vagas():
    """Exibe as vagas cadastradas pela empresa logada"""
    if 'usuario_id' not in session or session.get('tipo') != 'empresa':
        return redirect('/')
    
    from models.model_vagas import Vaga
    vagas = Vaga.listar_empresa(session['usuario_id'])
    
    return render_template('home/home_emp.html', vagas=vagas)
#======================================================================================================================================


#======================================================================================================================================

#excluir vaga
@bp_vagas.route('/vaga/excluir/<int:id_vaga>', methods=['POST'])
def excluir_vaga(id_vaga):
    """Exclui uma vaga com redirect"""
    if 'usuario_id' not in session or session.get('tipo') != 'empresa':
        flash("Acesso não autorizado!", "erro")
        return redirect('/')
    
    try:
        vaga = Vaga.buscar(id_vaga)
        if not vaga:
            flash("Vaga não encontrada!", "erro")
            return redirect(url_for('vagas.empresa_vagas'))
        
        if vaga['id_empresa'] != session['usuario_id']:
            flash("Acesso não autorizado!", "erro")
            return redirect('/')
        
        sucesso = Vaga.deletar(id_vaga)
        
        if sucesso:
            flash("Vaga excluída com sucesso!", "sucesso")
        else:
            flash("Erro ao excluir vaga!", "erro")
            
    except Exception as e:
        flash(f"Erro ao excluir vaga: {str(e)}", "erro")
    
    return redirect(url_for('vagas.empresa_vagas'))
