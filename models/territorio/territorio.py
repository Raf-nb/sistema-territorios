#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo para representar um território.
"""

import sqlite3
from typing import List, Dict, Any, Optional
from models.base_model import BaseModel

class Territorio(BaseModel):
    """Modelo para representar um território."""
    
    _table = "territorios"
    _columns = ["id", "nome", "descricao", "ultima_visita", "data_criacao"]
    
    def __init__(self, id: int = None, nome: str = "", descricao: str = "", 
                 ultima_visita: str = None, data_criacao: str = None):
        """
        Inicializa um território.
        
        Args:
            id (int, opcional): ID do território.
            nome (str, opcional): Nome do território.
            descricao (str, opcional): Descrição do território.
            ultima_visita (str, opcional): Data da última visita ao território.
            data_criacao (str, opcional): Data de criação do território.
        """
        super().__init__(
            id=id,
            nome=nome,
            descricao=descricao,
            ultima_visita=ultima_visita,
            data_criacao=data_criacao
        )
        
        # Campos calculados ou relacionados que não estão diretamente na tabela
        self.total_ruas = 0
        self.total_imoveis = 0
        self.ruas = []
    
    def get_ruas(self, db_manager) -> List[Dict[str, Any]]:
        """
        Obtém todas as ruas do território.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            
        Returns:
            List[Dict[str, Any]]: Lista de ruas do território.
        """
        if self.id is not None:
            cursor = db_manager.execute(
                "SELECT * FROM ruas WHERE territorio_id = ? ORDER BY nome",
                (self.id,)
            )
            if cursor:
                return [dict(row) for row in cursor.fetchall()]
        return []
    
    def add_rua(self, db_manager, nome_rua: str) -> bool:
        """
        Adiciona uma nova rua ao território.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            nome_rua (str): Nome da rua a ser adicionada.
            
        Returns:
            bool: True se a operação foi bem-sucedida, False caso contrário.
        """
        if self.id is not None:
            cursor = db_manager.execute(
                "INSERT INTO ruas (territorio_id, nome) VALUES (?, ?)",
                (self.id, nome_rua)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def get_estatisticas(self, db_manager) -> Dict[str, Any]:
        """
        Obtém estatísticas do território.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            
        Returns:
            Dict[str, Any]: Dicionário com estatísticas do território.
        """
        estatisticas = {
            "id": self.id,
            "nome": self.nome,
            "total_ruas": 0,
            "total_imoveis": 0,
            "total_atendimentos": 0,
            "cobertura_percentual": 0
        }
        
        # Total de ruas
        cursor = db_manager.execute(
            "SELECT COUNT(*) as total FROM ruas WHERE territorio_id = ?",
            (self.id,)
        )
        if cursor:
            estatisticas["total_ruas"] = cursor.fetchone()["total"]
        
        # Total de imóveis
        cursor = db_manager.execute(
            """
            SELECT COUNT(*) as total 
            FROM imoveis i 
            JOIN ruas r ON i.rua_id = r.id 
            WHERE r.territorio_id = ?
            """,
            (self.id,)
        )
        if cursor:
            estatisticas["total_imoveis"] = cursor.fetchone()["total"]
        
        # Total de atendimentos
        cursor = db_manager.execute(
            """
            SELECT COUNT(*) as total 
            FROM atendimentos a
            JOIN imoveis i ON a.imovel_id = i.id
            JOIN ruas r ON i.rua_id = r.id
            WHERE r.territorio_id = ?
            """,
            (self.id,)
        )
        if cursor:
            estatisticas["total_atendimentos"] = cursor.fetchone()["total"]
        
        # Contagem de imóveis únicos atendidos
        if estatisticas["total_imoveis"] > 0:
            cursor = db_manager.execute(
                """
                SELECT COUNT(DISTINCT a.imovel_id) as total
                FROM atendimentos a
                JOIN imoveis i ON a.imovel_id = i.id
                JOIN ruas r ON i.rua_id = r.id
                WHERE r.territorio_id = ?
                """,
                (self.id,)
            )
            if cursor:
                imoveis_atendidos = cursor.fetchone()["total"]
                estatisticas["cobertura_percentual"] = round(
                    (imoveis_atendidos / estatisticas["total_imoveis"]) * 100, 2
                )
        
        return estatisticas
    
    def atualizar_ultima_visita(self, db_manager, data_visita: str) -> bool:
        """
        Atualiza a data da última visita ao território.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            data_visita (str): Data da visita no formato 'YYYY-MM-DD'.
            
        Returns:
            bool: True se a operação foi bem-sucedida, False caso contrário.
        """
        if self.id is not None:
            self.ultima_visita = data_visita
            return self.save(db_manager)
        return False
    
    def __str__(self) -> str:
        """
        Retorna uma representação em string do território.
        
        Returns:
            str: Representação em string.
        """
        return self.nome if self.nome else "Território sem nome"