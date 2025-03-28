#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
import sqlite3
from models.base_model import BaseModel

class LogAtividade(BaseModel):
    """Modelo para representar um registro de atividade no sistema"""
    
    # Tipos de ação
    ACAO_LOGIN = "login"
    ACAO_LOGOUT = "logout"
    ACAO_CRIAR = "criar"
    ACAO_EDITAR = "editar"
    ACAO_EXCLUIR = "excluir"
    ACAO_VISUALIZAR = "visualizar"
    
    def __init__(self, id: int = None, usuario_id: int = None, 
                 tipo_acao: str = "", descricao: str = "",
                 data_hora: str = None, entidade: str = None,
                 entidade_id: int = None):
        super().__init__(id)
        self.usuario_id = usuario_id
        self.tipo_acao = tipo_acao
        self.descricao = descricao
        self.data_hora = data_hora
        self.entidade = entidade  # tipo de entidade (território, designação, etc.)
        self.entidade_id = entidade_id  # id da entidade, se aplicável
        
        # Campos extras para exibição
        self.usuario_nome = None
    
    @staticmethod
    def from_db_row(row: sqlite3.Row) -> 'LogAtividade':
        """Cria um objeto LogAtividade a partir de uma linha do banco de dados"""
        log = LogAtividade(
            id=row['id'],
            usuario_id=row['usuario_id'],
            tipo_acao=row['tipo_acao'],
            descricao=row['descricao'],
            data_hora=row['data_hora'],
            entidade=row['entidade'],
            entidade_id=row['entidade_id']
        )
        
        # Adiciona campos extras se estiverem disponíveis
        if 'usuario_nome' in row.keys():
            log.usuario_nome = row['usuario_nome']
            
        return log
    
    @staticmethod
    def get_all(db_manager, limit: int = 100) -> List['LogAtividade']:
        """Obtém todos os registros de atividade do banco de dados"""
        cursor = db_manager.execute(
            "SELECT l.*, u.nome as usuario_nome FROM log_atividades l "
            "LEFT JOIN usuarios u ON l.usuario_id = u.id "
            "ORDER BY l.data_hora DESC LIMIT ?",
            (limit,)
        )
        if cursor:
            return [LogAtividade.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_by_usuario(db_manager, usuario_id: int, limit: int = 50) -> List['LogAtividade']:
        """Obtém os registros de atividade de um usuário específico"""
        cursor = db_manager.execute(
            "SELECT l.*, u.nome as usuario_nome FROM log_atividades l "
            "LEFT JOIN usuarios u ON l.usuario_id = u.id "
            "WHERE l.usuario_id = ? "
            "ORDER BY l.data_hora DESC LIMIT ?",
            (usuario_id, limit)
        )
        if cursor:
            return [LogAtividade.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_by_entidade(db_manager, entidade: str, entidade_id: int = None, limit: int = 50) -> List['LogAtividade']:
        """Obtém os registros de atividade de uma entidade específica"""
        query = "SELECT l.*, u.nome as usuario_nome FROM log_atividades l " \
                "LEFT JOIN usuarios u ON l.usuario_id = u.id " \
                "WHERE l.entidade = ? "
        params = [entidade]
        
        if entidade_id is not None:
            query += "AND l.entidade_id = ? "
            params.append(entidade_id)
        
        query += "ORDER BY l.data_hora DESC LIMIT ?"
        params.append(limit)
        
        cursor = db_manager.execute(query, params)
        if cursor:
            return [LogAtividade.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def registrar(db_manager, usuario_id: int, tipo_acao: str, 
                 descricao: str, entidade: str = None, entidade_id: int = None) -> bool:
        """Registra uma nova atividade no sistema"""
        cursor = db_manager.execute(
            "INSERT INTO log_atividades (usuario_id, tipo_acao, descricao, entidade, entidade_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (usuario_id, tipo_acao, descricao, entidade, entidade_id)
        )
        if cursor:
            db_manager.commit()
            return True
        return False
    
    def __str__(self) -> str:
        usuario = f" por {self.usuario_nome}" if self.usuario_nome else ""
        return f"{self.tipo_acao.capitalize()}{usuario}: {self.descricao}"