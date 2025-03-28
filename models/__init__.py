# models/__init__.py
"""
Pacote para os modelos de dados do Sistema de Controle de Territórios
"""

from models.base_model import BaseModel
from models.territorio import Territorio
from models.rua import Rua

__all__ = [
    'BaseModel',
    'Territorio',
    'Rua'
]