# models/usuario/__init__.py
"""
Módulo para modelos relacionados a usuários
"""
from models.usuario.usuario import Usuario
from models.usuario.notificacao import Notificacao

__all__ = ['Usuario', 'Notificacao']