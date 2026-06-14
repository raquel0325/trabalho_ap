# models/__init__.py
"""
Módulo de Models - Regras de negócio
"""

from models.model_comp import Competencia
from models.model_emp import Empresa
from models.model_fun import Funcionario
from models.model_quest import Questionario
from models.model_vagas import Vaga, Candidatura, Match

__all__ = [
    'Competencia',
    'Empresa',
    'Funcionario', 
    'Questionario',
    'Vaga',
    'Candidatura',
    'Match'
]