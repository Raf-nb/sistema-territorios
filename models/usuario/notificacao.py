#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional, Dict, Any
import sqlite3
from datetime import datetime
from models.base_model import BaseModel
from models.usuario.usuario import Usuario

class Notificacao(BaseModel):
    """Modelo para representar uma notificação para um usuário"""
    
    # Tipos de notificação
    TIPO_INFO = "info"
    TIPO_ALERTA = "alerta"
    TIPO_ERRO = "erro"
    
    # Status da notificação
    STATUS_NAO_LIDA = "nao_lida"
    STATUS_LIDA = "lida"
    STATUS_ARQUIVADA = "arquivada"
    
    def __init__(self, id: int = None, usuario_id: int = None,
                 tipo: str = TIPO_INFO, titulo: str = "",
                 mensagem: str = "", status: str = STATUS_NAO_LIDA,
                 data_criacao: str = None, data_leitura: str = None,
                 link: str = None, entidade: str = None, 
                 entidade_id: int = None):
        super().__init__(id)
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.titulo = titulo
        self.mensagem = mensagem
        self.status = status
        self.data_criacao = data_criacao
        self.data_leitura = data_leitura
        self.link = link  # link/ação relacionada à notificação
        self.entidade = entidade  # tipo de entidade relacionada
        self.entidade_id = entidade_id  # id da entidade, se aplicável
    
    @staticmethod
    def from_db_row(row: sqlite3.Row) -> 'Notificacao':
        """Cria um objeto Notificacao a partir de uma linha do banco de dados"""
        return Notificacao(
            id=row['id'],
            usuario_id=row['usuario_id'],
            tipo=row['tipo'],
            titulo=row['titulo'],
            mensagem=row['mensagem'],
            status=row['status'],
            data_criacao=row['data_criacao'],
            data_leitura=row['data_leitura'],
            link=row['link'],
            entidade=row['entidade'],
            entidade_id=row['entidade_id']
        )
    
    @staticmethod
    def get_by_id(db_manager, notificacao_id: int) -> Optional['Notificacao']:
        """Obtém uma notificação pelo ID"""
        cursor = db_manager.execute(
            "SELECT * FROM notificacoes WHERE id = ?",
            (notificacao_id,)
        )
        if cursor:
            row = cursor.fetchone()
            if row:
                return Notificacao.from_db_row(row)
        return None
    
    @staticmethod
    def get_by_usuario(db_manager, usuario_id: int, apenas_nao_lidas: bool = False) -> List['Notificacao']:
        """Obtém as notificações de um usuário específico"""
        query = "SELECT * FROM notificacoes WHERE usuario_id = ?"
        params = [usuario_id]
        
        if apenas_nao_lidas:
            query += " AND status = ?"
            params.append(Notificacao.STATUS_NAO_LIDA)
        
        query += " ORDER BY data_criacao DESC"
        
        cursor = db_manager.execute(query, params)
        if cursor:
            return [Notificacao.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def criar(db_manager, usuario_id: int, tipo: str, titulo: str, 
              mensagem: str, link: str = None, entidade: str = None, 
              entidade_id: int = None) -> bool:
        """Cria uma nova notificação para um usuário"""
        cursor = db_manager.execute(
            "INSERT INTO notificacoes (usuario_id, tipo, titulo, mensagem, status, link, entidade, entidade_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (usuario_id, tipo, titulo, mensagem, Notificacao.STATUS_NAO_LIDA, link, entidade, entidade_id)
        )
        if cursor:
            db_manager.commit()
            return True
        return False
    
    @staticmethod
    def criar_para_todos(db_manager, tipo: str, titulo: str, 
                        mensagem: str, link: str = None, entidade: str = None, 
                        entidade_id: int = None) -> bool:
        """Cria uma notificação para todos os usuários ativos"""
        # Obtém todos os usuários ativos
        usuarios = Usuario.get_ativos(db_manager)
        if not usuarios:
            return False
        
        # Cria a notificação para cada usuário
        for usuario in usuarios:
            Notificacao.criar(
                db_manager, usuario.id, tipo, titulo, mensagem, 
                link, entidade, entidade_id
            )
        
        return True
    
    def marcar_como_lida(self, db_manager) -> bool:
        """Marca a notificação como lida"""
        if self.id is not None and self.status == Notificacao.STATUS_NAO_LIDA:
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = db_manager.execute(
                "UPDATE notificacoes SET status = ?, data_leitura = ? "
                "WHERE id = ?",
                (Notificacao.STATUS_LIDA, agora, self.id)
            )
            if cursor:
                self.status = Notificacao.STATUS_LIDA
                self.data_leitura = agora
                db_manager.commit()
                return True
        return False
    
    def arquivar(self, db_manager) -> bool:
        """Arquiva a notificação"""
        if self.id is not None:
            cursor = db_manager.execute(
                "UPDATE notificacoes SET status = ? WHERE id = ?",
                (Notificacao.STATUS_ARQUIVADA, self.id)
            )
            if cursor:
                self.status = Notificacao.STATUS_ARQUIVADA
                db_manager.commit()
                return True
        return False
    
    def __str__(self) -> str:
        return f"{self.titulo}: {self.mensagem}"