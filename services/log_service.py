#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Any, Optional
from models.log.log_atividade import LogAtividade

class LogService:
    """Serviço para gerenciar logs do sistema"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def registrar_atividade(self, usuario_id: int, tipo_acao: str, 
                           descricao: str, entidade: str = None, 
                           entidade_id: int = None) -> bool:
        """Registra uma atividade no sistema"""
        return LogAtividade.registrar(
            self.db_manager,
            usuario_id,
            tipo_acao,
            descricao,
            entidade,
            entidade_id
        )
    
    def registrar_login(self, usuario_id: int, nome_usuario: str) -> bool:
        """Registra uma atividade de login"""
        return self.registrar_atividade(
            usuario_id, 
            LogAtividade.ACAO_LOGIN, 
            f"Login realizado por {nome_usuario}",
            "usuario",
            usuario_id
        )
    
    def registrar_logout(self, usuario_id: int, nome_usuario: str) -> bool:
        """Registra uma atividade de logout"""
        return self.registrar_atividade(
            usuario_id, 
            LogAtividade.ACAO_LOGOUT, 
            f"Logout realizado por {nome_usuario}",
            "usuario",
            usuario_id
        )
    
    def registrar_criacao(self, usuario_id: int, entidade: str, 
                         descricao: str, entidade_id: int = None) -> bool:
        """Registra uma atividade de criação"""
        return self.registrar_atividade(
            usuario_id, 
            LogAtividade.ACAO_CRIAR, 
            descricao,
            entidade,
            entidade_id
        )
    
    def registrar_edicao(self, usuario_id: int, entidade: str, 
                        descricao: str, entidade_id: int = None) -> bool:
        """Registra uma atividade de edição"""
        return self.registrar_atividade(
            usuario_id, 
            LogAtividade.ACAO_EDITAR, 
            descricao,
            entidade,
            entidade_id
        )
    
    def registrar_exclusao(self, usuario_id: int, entidade: str, 
                          descricao: str, entidade_id: int = None) -> bool:
        """Registra uma atividade de exclusão"""
        return self.registrar_atividade(
            usuario_id, 
            LogAtividade.ACAO_EXCLUIR, 
            descricao,
            entidade,
            entidade_id
        )
    
    def registrar_visualizacao(self, usuario_id: int, entidade: str, 
                              descricao: str, entidade_id: int = None) -> bool:
        """Registra uma atividade de visualização"""
        return self.registrar_atividade(
            usuario_id, 
            LogAtividade.ACAO_VISUALIZAR, 
            descricao,
            entidade,
            entidade_id
        )
    
    def get_log_usuario(self, usuario_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtém o log de atividades de um usuário específico"""
        return LogAtividade.get_by_usuario(self.db_manager, usuario_id, limit)
    
    def get_ultimos_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtém os últimos registros de log do sistema"""
        return LogAtividade.get_all(self.db_manager, limit)