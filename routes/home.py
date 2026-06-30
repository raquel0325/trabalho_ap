from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from database.connect import get_connection
from CRUDs.candidatura import CandidaturaCRUD, MatchCRUD
from CRUDs.crud_quest import QuestionarioCRUD
from CRUDs.crud_func import FuncionarioCRUD
from CRUDs.crud_contratar import ContratacaoCRUD
from models.model_freelancer import Freelancer
from models.model_contratar import Contratacao
from models.model_comp import Competencia
from models.model_vagas import Vaga, Candidatura, Match
from models.model_emp import Empresa
from models.model_fun import Funcionario
from models.model_notificacao import Notificacao

bp_home = Blueprint('home', __name__)
#======================================================================================================================================


#======================================================================================================================================

@bp_home.route('/home')
def home_pag():
    """Página inicial após login"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    tipo = session.get('tipo')
    id_usuario = session.get('usuario_id')
    notificacoes = Notificacao.listar_para_usuario(id_usuario, apenas_nao_lidas=False, limite=4)
    if tipo == 'funcionario':
        
        candidaturas = CandidaturaCRUD.listar_candidaturas_funcionario(id_usuario)# Busca candidaturas
        vagas_recomendadas = Match.melhores_vagas(id_usuario, limite=5)# Busca vagas recomendadas
        funcionario = FuncionarioCRUD.buscar_por_id(id_usuario)# Busca dados do funcionário
        questionario = QuestionarioCRUD.buscar_por_funcionario(id_usuario)# Busca dados do questionário
        competencias_usuario = Competencia.listar_do_funcionario(id_usuario)#  BUSCA AS COMPETÊNCIAS DO USUÁRIO 
        todas_competencias = Competencia.listar_todas()# Busca todas as competências disponíveis
        contratacoes = Contratacao.listar_contratacao(id_usuario)# Busca contratos
        meus_freelances = Freelancer.listar_por_funcionario(id_usuario)# Busca meus freelances
        contratados = ContratacaoCRUD.listar_contratados(id_usuario)# Atualiza sessão
            
        contratados_lista = []

        for contrato in contratados:
                contrato_dict = dict(contrato)
                contrato_dict["avaliado"] = ContratacaoCRUD.buscar_avaliacao(
                    contrato_dict["id_freelancer"],
                    id_usuario,
                    contrato_dict["tipo_contratante"]
                )
                contratados_lista.append(contrato_dict)

        contratados = contratados_lista
        if funcionario:
            session['usuario_nome'] = funcionario.get('nome')
    
        return render_template('home/home_func.html', nome=session.get('usuario_nome'), tipo=tipo,
                             candidaturas=candidaturas,vagas_recomendadas=vagas_recomendadas,
                             funcionario=funcionario,questionario=questionario,
                             competencias_usuario=competencias_usuario,
                             todas_competencias=todas_competencias,
                             contratacoes=contratacoes,meus_freelances=meus_freelances,
                             contratados=contratados, notificacoes=notificacoes)    
    
    
    elif tipo == 'empresa':
            
            empresa = Empresa.buscar_por_id(id_usuario)
            vagas = Vaga.listar_empresa(id_usuario)

            contratados = ContratacaoCRUD.listar_contratados(id_usuario)

            # Notificações da empresa (id_usuario = id_empresa na sessão)
            notificacoes = Notificacao.listar_para_usuario(id_usuario, apenas_nao_lidas=False, limite=4)


            # id_contratante = id_usuario
            contratados_lista = []
            for contrato in contratados:
                contrato_dict = dict(contrato)
                contrato_dict["avaliado"] = ContratacaoCRUD.buscar_avaliacao(
                    contrato_dict["id_freelancer"],
                    id_usuario,
                    contrato_dict["tipo_contratante"]
                )
                contratados_lista.append(contrato_dict)

            contratados = contratados_lista

            if empresa and empresa.get('nome'):
                session['usuario_nome'] = empresa.get('nome')

            return render_template(
                'home/home_emp.html',
                nome=session.get('usuario_nome'),
                tipo=tipo,
                empresa=empresa,
                vagas=vagas,
                contratados=contratados,
                notificacoes=notificacoes
            )

#======================================================================================================================================


#======================================================================================================================================
@bp_home.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    return redirect('/')
#======================================================================================================================================


#======================================================================================================================================


@bp_home.route('/excluir_perfil', methods=['POST'])
def excluir_perfil():
    if 'usuario_id' not in session:
        return redirect('/')

    usuario_id = session['usuario_id']
    tipo = session.get('tipo')

    try:
        if tipo == 'funcionario':
            Funcionario.excluir_perfil(usuario_id)
        elif tipo == 'empresa':
            Empresa.excluir_perfil(usuario_id)
        else:
            flash('Tipo de usuário inválido.', 'erro')
            return redirect(url_for('home.home_pag'))
        session.clear()
        flash('Perfil excluído com sucesso!', 'sucesso')
        return redirect('/')

    except Exception as e:
        flash(f'Erro ao excluir perfil: {str(e)}', 'erro')
        return redirect(url_for('home.home_pag'))
#======================================================================================================================================


#======================================================================================================================================
