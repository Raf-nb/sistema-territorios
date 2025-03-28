# database/__init__.py
"""
Módulo para gerenciamento do banco de dados
"""
from database.db_manager import DatabaseManager
from database.backup import backup_database

__all__ = ['DatabaseManager', 'backup_database']