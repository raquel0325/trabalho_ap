# CRUDs/__init__.py
"""
Módulo de CRUDs para operações de banco de dados
"""

from CRUDs.crud_comp import CompetenciaCRUD
from CRUDs.crud_emp import EmpresaCRUD
from CRUDs.crud_func import FuncionarioCRUD
from CRUDs.crud_quest import QuestionarioCRUD
from CRUDs.crud_vagas import VagaCRUD
from CRUDs.candidatura import CandidaturaCRUD, MatchCRUD
from CRUDs.crud_freelancer import FreelancerCRUD
from CRUDs.crud_avaliacao import AvaliacaoCRUD
from CRUDs.crud_contratar import ContratacaoCRUD

__all__ = [
    'CompetenciaCRUD',
    'EmpresaCRUD', 
    'FuncionarioCRUD',
    'QuestionarioCRUD',
    'VagaCRUD',
    'CandidaturaCRUD',
    'MatchCRUD',
    'FreelancerCRUD',
    'AvaliacaoCRUD',
    'ContratacaoCRUD'
]