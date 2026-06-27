from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.model_contratar import Contratacao
from CRUDs.crud_freelancer import FreelancerCRUD
from CRUDs.crud_contratar import ContratacaoCRUD

bp_solicitantes = Blueprint('solicitantes', __name__)


# ─────────────────────────────────────────────────────────────────
# ROTA: freelancer vê quem solicitou seu serviço
# ─────────────────────────────────────────────────────────────────
@bp_solicitantes.route('/freelancer/<int:id_freelancer>/solicitantes')
def ver_solicitantes(id_freelancer):
    """
    Exibe todos os solicitantes de um freelancer.
    Apenas o funcionário dono do freelancer pode acessar.
    """
    if 'usuario_id' not in session:
        return redirect('/')

    if session.get('tipo') != 'funcionario':
        flash('Acesso não permitido.', 'erro')
        return redirect(url_for('home.home_pag'))

    id_funcionario = session['usuario_id']

    # Confirma que o freelancer pertence ao funcionário logado
    freelance = FreelancerCRUD.buscar_por_id(id_freelancer)
    if not freelance or freelance['id_funcionario'] != id_funcionario:
        flash('Freelancer não encontrado ou sem permissão.', 'erro')
        return redirect(url_for('home.home_pag'))

    solicitantes = ContratacaoCRUD.listar_solicitantes(id_freelancer)

    return render_template(
        'home/ver_solicitantes.html',
        freelance=freelance,
        solicitantes=solicitantes
    )


# ─────────────────────────────────────────────────────────────────
# ROTA: freelancer atualiza o status de uma contratação
# ─────────────────────────────────────────────────────────────────
@bp_solicitantes.route('/contratacao/<int:id_contratacao>/status', methods=['POST'])
def atualizar_status(id_contratacao):
    """
    Atualiza o status de uma contratação.
    Somente o funcionário dono do freelancer pode chamar esta rota.
    """
    if 'usuario_id' not in session:
        return redirect('/')

    if session.get('tipo') != 'funcionario':
        flash('Acesso não permitido.', 'erro')
        return redirect(url_for('home.home_pag'))

    id_funcionario = session['usuario_id']
    novo_status = request.form.get('status')

    statuses_validos = {'pendente', 'aceito', 'recusado', 'concluido', 'cancelado'}
    if novo_status not in statuses_validos:
        flash('Status inválido.', 'erro')
        return redirect(request.referrer or url_for('home.home_pag'))

    sucesso = ContratacaoCRUD.atualizar_status(id_contratacao, novo_status, id_funcionario)

    if sucesso:
        flash(f'Status atualizado para "{novo_status}" com sucesso!', 'sucesso')
    else:
        flash('Erro ao atualizar status. Verifique sua permissão.', 'erro')

    # Volta para a página de solicitantes do freelancer correto
    contratacao = ContratacaoCRUD.buscar_por_id(id_contratacao)
    if contratacao:
        return redirect(url_for('solicitantes.ver_solicitantes',
                                id_freelancer=contratacao['id_freelancer']))

    return redirect(url_for('home.home_pag'))