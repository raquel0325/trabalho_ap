from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.model_freelancer import Freelancer
from CRUDs.crud_freelancer import FreelancerCRUD 
from CRUDs.crud_contratar import ContratacaoCRUD
from models.model_avaliacao import Avaliacao



bp_freelancer = Blueprint('freelancer', __name__)

@bp_freelancer.route('/freelancer', methods=['GET', 'POST'])

    
def buscar_freelancer():
    if 'usuario_id' not in session:
        return redirect('/')
    
    id_usuario = session['usuario_id']
    tipo_usuario = session.get('tipo')

    busca = request.args.get('busca', '')
    disponibilidade = request.args.get('disponibilidade', '')
    preco_medio_min = request.args.get('preco_medio_min', '')
    preco_medio_max = request.args.get('preco_medio_max', '')
    
    try:
        preco_medio_min = float(preco_medio_min) if preco_medio_min else None
    except ValueError:
        preco_medio_min = None
    
    try:
        preco_medio_max = float(preco_medio_max) if preco_medio_max else None
    except ValueError:
        preco_medio_max = None

    resultado = Freelancer.buscar_freelancer(busca=busca if busca else None,
                                             disponibilidade=disponibilidade if disponibilidade else None,
                                             preco_medio_min=preco_medio_min,preco_medio_max=preco_medio_max)
    freelancers_com_status = []
    for freelancer in resultado:
        freelancer_dict = dict(freelancer)
        tipo_contratante = session['tipo']
        
        # Verifica se o usuário já contratou este freelancer
        if tipo_usuario == 'empresa' or tipo_usuario == 'funcionario':
            contratacao = ContratacaoCRUD.buscar_por_freelancer_e_contratante(
                freelancer['id_freelancer'], 
                id_usuario,
                tipo_contratante
                )
            freelancer_dict['ja_contratou'] = contratacao is not None
            
            # Se contratou, busca a média das avaliações
            media_info = Avaliacao.calcular_media_avaliacoes(freelancer['id_freelancer'])

            freelancer_dict['media_avaliacao'] = media_info['media']
            freelancer_dict['total_avaliacoes'] = media_info['total']

            freelancer_dict['ja_contratou'] = contratacao is not None
            
            freelancers_com_status.append(freelancer_dict)
    
    return render_template('vaga/freelancer_listar.html',resultado=freelancers_com_status,busca=busca,
                           disponibilidade=disponibilidade,preco_medio_min=preco_medio_min,preco_medio_max=preco_medio_max,
                           tipo_usuario=tipo_usuario)
#====================================================================================================================================



#==================================================================================================================================



@bp_freelancer.route('/freelancer/cadastrar', methods=['POST'])
def cadastrar_freelance():
    if 'usuario_id' not in session:
        return redirect('/')

    if session.get('tipo') != 'funcionario':
        return redirect('/')

    id_funcionario = session['usuario_id']

    profissao = request.form.get('profissao')
    servico_oferecido = request.form.get('servico_oferecido')
    preco_medio = request.form.get('preco_medio')
    disponibilidade = request.form.get('disponibilidade', 'disponivel')

    if not profissao or not servico_oferecido:
        flash("Preencha todos os campos obrigatórios!", "erro")
        return redirect(url_for('home.home_pag'))

    try:
        preco_medio = float(preco_medio) if preco_medio else 0
    except ValueError:
        preco_medio = 0

    try:
        freelancer_id = FreelancerCRUD.inserir(profissao=profissao,servico_oferecido=servico_oferecido,
            preco_medio=preco_medio,disponibilidade=disponibilidade,id_funcionario=id_funcionario)

        print("Freelancer criado:", freelancer_id)

        flash("Freelance cadastrado com sucesso!", "sucesso")

    except Exception as e:

        flash(f"Erro ao cadastrar freelance: {str(e)}", "erro")

    return redirect(url_for('home.home_pag'))


#======================================================================================================================================


#======================================================================================================================================

@bp_freelancer.route('/freelancer/editar/<int:id_freelancer>', methods=['GET', 'POST'])
def editar_freelance(id_freelancer):

    if 'usuario_id' not in session:
        return redirect('/')

    if session.get('tipo') != 'funcionario':
        return redirect('/')

    id_funcionario = session['usuario_id']

    freelance = FreelancerCRUD.buscar_por_id(id_freelancer)

    if not freelance:
        flash("Freelancer não encontrado", "erro")
        return redirect(url_for('home.home_pag'))

    # segurança
    if freelance['id_funcionario'] != id_funcionario:
        flash("Você não tem permissão para editar este registro", "erro")
        return redirect(url_for('home.home_pag'))

    if request.method == 'POST':
        try:
            profissao = request.form.get('profissao')
            servico_oferecido = request.form.get('servico_oferecido')
            preco_medio = request.form.get('preco_medio')
            disponibilidade = request.form.get('disponibilidade')

            if not profissao or not servico_oferecido:
                flash("Campos obrigatórios não preenchidos", "erro")
                return render_template('vaga/editar_freelance.html', freelance=freelance)

            preco_medio = float(preco_medio) if preco_medio else 0

            # UPDATE
            rowcount = FreelancerCRUD.atualizar(
                id_freelancer=id_freelancer,
                profissao=profissao,
                servico_oferecido=servico_oferecido,
                preco_medio=preco_medio,
                disponibilidade=disponibilidade
            )

            if rowcount == 0:
                flash("Nada foi atualizado (ID pode não existir)", "erro")
            else:
                flash("Freelancer atualizado com sucesso!", "sucesso")

            return redirect(url_for('home.home_pag'))

        except Exception as e:
            flash(f'Erro ao atualizar: {str(e)}', 'erro')

    return render_template('vaga/editar_freelance.html', freelance=freelance)


#================================================================================================================================================================

@bp_freelancer.route('/freelancer/excluir/<int:id_freelancer>', methods=['DELETE'])
def excluir_freelance(id_freelancer):

    if 'usuario_id' not in session:
        return {'success': False, 'message': 'Usuário não autenticado'}, 401

    if session.get('tipo') != 'funcionario':
        return {'success': False, 'message': 'Sem permissão'}, 403

    id_funcionario = session['usuario_id']

    try:
        freelance = FreelancerCRUD.buscar_por_id(id_freelancer)

        if not freelance:
            return {'success': False, 'message': 'Não encontrado'}, 404

        if freelance['id_funcionario'] != id_funcionario:
            return {'success': False, 'message': 'Sem permissão'}, 403

        deleted = FreelancerCRUD.deletar(id_freelancer)

        if deleted == 0:
            return {'success': False, 'message': 'Nada foi deletado'}, 404

        return {'success': True, 'message': 'Excluído com sucesso'}

    except Exception as e:
        return {'success': False, 'message': str(e)}, 500