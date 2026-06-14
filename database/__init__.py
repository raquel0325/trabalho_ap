# database/__init__.py
"""
Módulo de Database - Conexão e inicialização do banco
"""

from database.connect import get_connection, get_cursor
from database.main import init_db

__all__ = [
    'get_connection',
    'get_cursor', 
    'init_db'
]