from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from models.model_fun import Funcionario
from models.model_emp import Empresa

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/')
def pagina_inicial():
    """Página inicial com login e cadastro"""
    return render_template('index.html')

@bp_auth.route('/cadastro/funcionario', methods=['POST'])
def cadastrar_funcionario():
    """Cadastro de funcionário"""
    try:
        id_funcionario = Funcionario.cadastrar(
            nome=request.form.get('nome'),
            email=request.form.get('email'),
            senha=request.form.get('senha'),
            telefone=request.form.get('telefone'),
            cpf=request.form.get('cpf')
        )
        
        session['usuario_id'] = id_funcionario
        session['usuario_nome'] = request.form.get('nome')
        session['tipo'] = 'funcionario'

        flash("Cadastro realizado com sucesso!", "sucesso")
        return redirect(url_for('questionario.questionario_pag', 
                              id_func=id_funcionario))
        
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(str(e), "erro")
    
    return redirect('/')

@bp_auth.route('/cadastro/empresa', methods=['POST'])
def cadastrar_empresa():
    """Cadastro de empresa"""
    try:
        Empresa.cadastrar(
            nome=request.form.get('nome'),
            cnpj=request.form.get('cnpj'),
            email=request.form.get('email'),
            senha=request.form.get('senha'),
            telefone=request.form.get('telefone', ''),
            endereco=request.form.get('endereco', '')
        )
        
        flash("Empresa cadastrada com sucesso!", "sucesso")
    except ValueError as e:
        flash(str(e), "erro")
    except Exception as e:
        flash(str(e), "erro")
    
    return redirect('/')

@bp_auth.route('/login', methods=['POST'])
def login():
    """Login de funcionário ou empresa"""
    email = request.form.get('email')
    senha = request.form.get('senha')

    # Tenta login como funcionário
    usuario = Funcionario.autenticar(email, senha)
    if usuario:
        session['usuario_id'] = usuario['id']
        session['usuario_nome'] = usuario['nome']
        session['tipo'] = 'funcionario'
        return redirect(url_for('home.home_pag'))
    
    # Tenta login como empresa
    usuario = Empresa.autenticar(email, senha)
    if usuario:
        session['usuario_id'] = usuario['id']
        session['usuario_nome'] = usuario['nome']
        session['tipo'] = 'empresa'
        return redirect(url_for('home.home_pag'))

    flash("E-mail ou senha incorretos!", "erro")
    return redirect('/')