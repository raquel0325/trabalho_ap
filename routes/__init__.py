# routes/__init__.py
"""
Módulo de Rotas - Blueprints da aplicação
"""

from routes.auth import bp_auth
from routes.home import bp_home
from routes.questionario import bp_questionario
from routes.vagas import bp_vagas
from routes.google_auth import bp_google, init_oauth
from routes.candidatar_se import bp_candidatar_se
from routes.atualizar_vaga import bp_atualizar_vaga

__all__ = [
    'bp_auth',
    'bp_home', 
    'bp_questionario',
    'bp_vagas',
    'bp_google',
    'init_oauth',
    'bp_candidatar_se',
    'bp_atualizar_vaga'
]