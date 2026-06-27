from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.model_contratar import Contratacao



bp_contratar_frelas = Blueprint('contratar_frelas', __name__)



@bp_contratar_frelas.route('/contratar/<int:id_freelancer>', methods=['POST'])

def contratar(id_freelancer):
    if 'usuario_id' not in session:
        return redirect('/')

    id_contratante = session['usuario_id']
    tipo_contratante = session['tipo']


    sucesso = Contratacao.contratar_freelancer(
        id_freelancer,
        id_contratante,
        tipo_contratante,
    )

    if sucesso:
        flash('Freelancer contratado com sucesso!','sucesso')
    else:
        flash('Erro ao contratar freelancer.','erro')

    return redirect(url_for('freelancer.buscar_freelancer'))