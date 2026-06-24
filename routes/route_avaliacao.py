from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.model_avaliacao import Avaliacao
from CRUDs.crud_avaliacao import AvaliacaoCRUD
from models.model_freelancer import Freelancer
from CRUDs.crud_freelancer import FreelancerCRUD
from CRUDs.crud_contratar import ContratacaoCRUD

bp_avaliacao = Blueprint('avaliacao', __name__)

@bp_avaliacao.route('/avaliar/<int:id_freelancer>', methods=['POST'])
def avaliar_freelancer(id_freelancer):
    """Avalia um freelancer"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    id_contratante = session['usuario_id']
    tipo_contratante = session['tipo']
    
    nota = request.form.get('nota')
    comentario = request.form.get('comentario', '').strip()
    
    # Valida nota
    try:
        nota = int(nota)
        if nota < 1 or nota > 5:
            flash("A nota deve ser entre 1 e 5!", "erro")
            return redirect(request.referrer or url_for('home.home_pag'))
    except ValueError:
        flash("Nota inválida!", "erro")
        return redirect(request.referrer or url_for('home.home_pag'))
    
    # Verifica se o contratante já contratou este freelancer
    contratacao = ContratacaoCRUD.buscar_por_freelancer_e_contratante(id_freelancer, id_contratante)
    
    if not contratacao:
        flash("Você só pode avaliar freelancers que contratou!", "erro")
        return redirect(request.referrer or url_for('home.home_pag'))
    
    #verifica se o contratante já avaliou este freelancer
    avaliado = AvaliacaoCRUD.adicionar_avaliacao(id_freelancer, id_contratante,tipo_contratante,nota,comentario)

    if avaliado:
        print('já avaliado ----')


    # Adiciona a avaliação
    sucesso = Avaliacao.adicionar_avaliacao(
        id_freelancer=id_freelancer,
        id_contratante=id_contratante,
        tipo_contratante=tipo_contratante,
        nota=nota,
        comentario=comentario
    )
    
    if sucesso:
        flash("Avaliação enviada com sucesso! ⭐", "sucesso")
    else:
        flash("Erro ao enviar avaliação.", "erro")
    
    return redirect(request.referrer or url_for('home.home_pag'))


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bp_avaliacao.route('/avaliacoes/<int:id_freelancer>')
def ver_avaliacoes(id_freelancer):
    """Página para ver avaliações de um freelancer"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    # Busca o freelancer
    freelancer = FreelancerCRUD.buscar_por_id(id_freelancer)
    if not freelancer:
        flash("Freelancer não encontrado!", "erro")
        return redirect(url_for('home.home_pag'))
    
    # Busca as avaliações
    avaliacoes = Avaliacao.listar_avaliacoes_com_usuarios(id_freelancer)
    
    # Calcula a média
    media_info = Avaliacao.calcular_media_avaliacoes(id_freelancer)
    
    return render_template('vaga/ver-avaliacao.html',
                         freelancer=freelancer,
                         avaliacoes=avaliacoes,
                         media=media_info['media'],
                         total=media_info['total'])