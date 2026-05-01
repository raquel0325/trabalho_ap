from flask import Blueprint, url_for, redirect, session, flash
from authlib.integrations.flask_client import OAuth
import requests
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from models.model_fun import Funcionario

bp_google = Blueprint('google_auth', __name__)

oauth = OAuth()

def init_oauth(app):
    """Inicializa o OAuth com o app Flask"""
    oauth.register(
        name='google',
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        server_metadata_url=Config.GOOGLE_META_URL,
        client_kwargs={'scope': 'openid email profile'}
    )
    oauth.init_app(app)

@bp_google.route("/google-login")
def google_login():
    """Inicia login com Google"""
    redirect_uri = url_for('google_auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@bp_google.route('/signin-google')
def google_callback():
    """Callback do Google após login"""
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash("Erro ao obter informações do Google", "erro")
            return redirect('/')
        
        email = user_info.get('email')
        nome = user_info.get('name')
        
        funcionario = Funcionario.buscar_por_google(email)
        
        if funcionario:
            session['usuario_id'] = funcionario['id']
            session['usuario_nome'] = nome
            session['tipo'] = 'funcionario'
            flash(f"Bem-vindo de volta, {nome}!", "sucesso")
        else:
            novo_id = Funcionario.cadastrar_via_google(nome, email)
            session['usuario_id'] = novo_id
            session['usuario_nome'] = nome
            session['tipo'] = 'funcionario'
            flash("Cadastro realizado! Complete seus dados.", "info")
        
        return redirect(url_for('home.home_pag'))
        
    except Exception as e:
        print(f"Erro no login Google: {e}")
        flash("Erro ao fazer login com Google", "erro")
        return redirect('/')