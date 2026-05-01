from flask import Blueprint, render_template, session, redirect, url_for

bp_home = Blueprint('home', __name__)

@bp_home.route('/home')
def home_pag():
    """Página inicial após login"""
    if 'usuario_id' not in session:
        return redirect('/')
    
    tipo = session.get('tipo')
    nome = session.get('usuario_nome')
    
    if tipo == 'funcionario':
        return render_template('home_func.html', nome=nome, tipo=tipo)
    elif tipo == 'empresa':
        return render_template('home_emp.html', nome=nome, tipo=tipo)
    elif tipo == 'google':
        return render_template('home_func.html', nome=nome, tipo='google')
    
    return redirect('/')

@bp_home.route('/logout')
def logout():
    """Logout do usuário"""
    session.clear()
    return redirect('/')