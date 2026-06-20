from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from CRUDs.candidatura import CandidaturaCRUD, MatchCRUD
from models.model_vagas import Vaga, Candidatura, Match
from CRUDs.crud_quest import QuestionarioCRUD
from database.connect import get_connection
from CRUDs.crud_func import FuncionarioCRUD
from models.model_comp import Competencia
from CRUDs.crud_seguir import SeguirCRUD


bp_home = Blueprint('home', __name__)

@bp_home.route('/home')
def home_pag():
    """Página inicial após login"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    tipo = session.get('tipo')
    id_usuario = session.get('usuario_id')
    
    if tipo == 'funcionario':
        # Busca candidaturas
        candidaturas = CandidaturaCRUD.listar_candidaturas_funcionario(id_usuario)
        
        # Busca vagas recomendadas
        vagas_recomendadas = Match.melhores_vagas(id_usuario, limite=5)
        
        # Busca dados do funcionário
        funcionario = FuncionarioCRUD.buscar_por_id(id_usuario)
        
        # Busca dados do questionário
        questionario = QuestionarioCRUD.buscar_por_funcionario(id_usuario)
        
        #  BUSCA AS COMPETÊNCIAS DO USUÁRIO 

        competencias_usuario = Competencia.listar_do_funcionario(id_usuario)
        
        # Busca todas as competências disponíveis
        todas_competencias = Competencia.listar_todas()
        
        outros_usuarios = SeguirCRUD.listar_outros_usuarios(id_usuario)
        outros_usuarios_lista = [dict(usuario) for usuario in outros_usuarios] if outros_usuarios else []

        # Atualiza sessão
        if funcionario:
            session['usuario_nome'] = funcionario.get('nome')
        
        return render_template('home/home_func.html', 
                             nome=session.get('usuario_nome'), 
                             tipo=tipo,
                             candidaturas=candidaturas,
                             vagas_recomendadas=vagas_recomendadas,
                             funcionario=funcionario,
                             questionario=questionario,
                             competencias_usuario=competencias_usuario,
                             todas_competencias=todas_competencias,
                             outros_usuarios=outros_usuarios_lista)
    
    elif tipo == 'empresa':
        # Busca dados da empresa
        from models.model_emp import Empresa
        empresa = Empresa.buscar_por_id(id_usuario)
        
        # Busca vagas da empresa
        from models.model_vagas import Vaga
        vagas = Vaga.listar_empresa(id_usuario)
        
        # Atualiza sessão com o nome da empresa
        if empresa and empresa.get('nome'):
            session['usuario_nome'] = empresa.get('nome')
        
        return render_template('home/home_emp.html', 
                             nome=session.get('usuario_nome'), 
                             tipo=tipo,
                             empresa=empresa,
                             vagas=vagas)
    
    return redirect('/')
#======================================================================================================================================


#======================================================================================================================================
@bp_home.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    return redirect('/')
#======================================================================================================================================


#======================================================================================================================================
@bp_home.route('/atualizar_perfil', methods=['POST'])
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
@bp_home.route('/atualizar_competencias', methods=['POST'])
def atualizar_competencias():
    """Atualiza as competências do usuário"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    id_usuario = session['usuario_id']
    

    
    try:
        from CRUDs.crud_comp import CompetenciaCRUD
        from database.connect import get_connection
        
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
        import traceback
        traceback.print_exc()
        flash(f"Erro ao atualizar competências: {str(e)}", "erro")
    
    return redirect(url_for('home.home_pag'))

#======================================================================================================================================

@bp_home.route('/atualizar_empresa', methods=['POST'])
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