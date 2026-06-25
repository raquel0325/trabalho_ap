from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.model_emp import Empresa
from models.model_fun import Funcionario
from CRUDs.crud_emp import EmpresaCRUD
from CRUDs.crud_func import FuncionarioCRUD
from CRUDs.crud_quest import QuestionarioCRUD
from database.connect import get_connection
from CRUDs.crud_comp import CompetenciaCRUD
from CRUDs.crud_contratar import ContratacaoCRUD
from models.model_freelancer import Freelancer
from CRUDs.crud_freelancer import FreelancerCRUD
from CRUDs.crud_avaliacao import AvaliacaoCRUD

bp_atualizar_perfil = Blueprint('atualizar_perfil', __name__)



@bp_atualizar_perfil.route('/atualizar_perfil', methods=['POST'])
def atualizar_perfil():
    """Atualiza os dados do perfil do funcionário"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    id_usuario = session['usuario_id']
    
    try:
        # Atualiza dados na tabela funcionarios
        FuncionarioCRUD.atualizar(
            id_usuario,
            nome=request.form.get('nome'),
            telefone=request.form.get('telefone'),
            cpf=request.form.get('cpf')
        )
        
        # Verifica se já existe um questionário
        existente = QuestionarioCRUD.buscar_por_funcionario(id_usuario)
        
        if existente:
            # Atualiza questionário existente
            QuestionarioCRUD.atualizar(
                id_funcionario=id_usuario,
                cidade=request.form.get('cidade'),
                estado=request.form.get('estado'),
                formacao=request.form.get('formacao'),
                curso=request.form.get('curso'),
                instituicao=request.form.get('instituicao'),
                ultimo_cargo=request.form.get('ultimo_cargo'),
                ultima_empresa=request.form.get('ultima_empresa'),
                tempo_experiencia=request.form.get('tempo_experiencia')
            )
        else:
            # Insere novo questionário
            QuestionarioCRUD.inserir_resposta(
                id_funcionario=id_usuario,
                cidade=request.form.get('cidade'),
                estado=request.form.get('estado'),
                formacao=request.form.get('formacao'),
                curso=request.form.get('curso'),
                instituicao=request.form.get('instituicao'),
                ano_conclusao=None,
                ultimo_cargo=request.form.get('ultimo_cargo'),
                ultima_empresa=request.form.get('ultima_empresa'),
                tempo_experiencia=request.form.get('tempo_experiencia')
            )
        
        flash("Perfil atualizado com sucesso!", "sucesso")
        
    except Exception as e:
        flash(f"Erro ao atualizar: {str(e)}", "erro")
    
    return redirect(url_for('home.home_pag'))
#======================================================================================================================================


#======================================================================================================================================
@bp_atualizar_perfil.route('/atualizar_competencias', methods=['POST'])
def atualizar_competencias():
    """Atualiza as competências do usuário"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    id_usuario = session['usuario_id']
    
    try: 
        
        # Remove todas as competências atuais
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM funcionario_competencias WHERE id_funcionario = ?', (id_usuario,))
        print("✓ Competências antigas removidas")
        
        # Adiciona as novas competências selecionadas
        competencias_ids = request.form.getlist('competencias')
        for comp_id in competencias_ids:
            if comp_id and comp_id.isdigit():
                print(f"✓ Adicionando competência ID: {comp_id}")
                cursor.execute('INSERT INTO funcionario_competencias (id_funcionario, id_competencia) VALUES (?, ?)',
                             (id_usuario, int(comp_id)))
        
        # Adiciona novas competências
        novas_competencias = request.form.getlist('novas_competencias')
        for nome_comp in novas_competencias:
            nome_comp = nome_comp.strip()
            if nome_comp:
                print(f"✓ Processando nova competência: '{nome_comp}'")
                
                # Verifica se já existe
                cursor.execute('SELECT id_competencia FROM competencias WHERE nome = ?', (nome_comp,))
                existente = cursor.fetchone()
                
                if existente:
                    comp_id = existente['id_competencia']
                    print(f"  → Competência já existe, ID: {comp_id}")
                else:
                    cursor.execute('INSERT INTO competencias (nome) VALUES (?)', (nome_comp,))
                    comp_id = cursor.lastrowid
                    print(f"  → Nova competência criada, ID: {comp_id}")
                
                cursor.execute('INSERT INTO funcionario_competencias (id_funcionario, id_competencia) VALUES (?, ?)',
                             (id_usuario, comp_id))
        
        conn.commit()
        conn.close()
        

        flash("Competências atualizadas com sucesso!", "sucesso")
        
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        flash(f"Erro ao atualizar competências: {str(e)}", "erro")
    
    return redirect(url_for('home.home_pag'))


#======================================================================================================================================


#======================================================================================================================================

@bp_atualizar_perfil.route('/atualizar_empresa', methods=['POST'])
def atualizar_empresa():
    """Atualiza os dados da empresa"""
    if 'usuario_id' not in session or session.get('tipo') != 'empresa':
        return redirect('/')
    
    id_usuario = session['usuario_id']
    
    try:
        from models.model_emp import Empresa
        
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        
        # Atualiza os dados
        Empresa.atualizar_perfil(
            id_empresa=id_usuario,
            nome=nome,
            email=email,
            telefone=telefone,
            endereco=endereco
        )
        
        # Atualiza a sessão com os novos dados
        if nome:
            session['usuario_nome'] = nome
        if email:
            session['usuario_email'] = email
        if telefone:
            session['usuario_telefone'] = telefone
        
        flash("Perfil atualizado com sucesso!", "sucesso")
        
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(f"Erro ao atualizar: {str(e)}", "erro")
    
    return redirect(url_for('home.home_pag'))

