# routes/__init__.py
"""
Módulo de Rotas - Blueprints da aplicação
"""

from routes.auth import bp_auth
from routes.home import bp_home
from routes.questionario import bp_questionario
from routes.route_vagas import bp_vagas
from routes.google_auth import bp_google, init_oauth
from routes.candidatar_se import bp_candidatar_se
from routes.atualizar_vaga import bp_atualizar_vaga
from routes.route_freelancer import bp_freelancer
from routes.route_avaliacao import bp_avaliacao
from routes.route_contratarfreelas import bp_contratar_frelas
from routes.atualizar_perfil import bp_atualizar_perfil
from routes.route_solicitante import bp_solicitantes

# Vitrine de autônomos
from routes.route_vitrine import bp_vitrine


__all__ = [
    'bp_auth',
    'bp_home',
    'bp_questionario',
    'bp_vagas',
    'bp_google',
    'init_oauth',
    'bp_candidatar_se',
    'bp_atualizar_vaga',
    'bp_freelancer',
    'bp_avaliacao',
    'bp_contratar_frelas',
    'bp_atualizar_perfil',
    'bp_solicitantes',
    'bp_vitrine'
]
