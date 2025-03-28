#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo para representar uma rua.
"""

import sqlite3
from typing import List, Dict, Any, Optional
from models.base_model import BaseModel

class Rua(BaseModel):
    """Modelo para representar uma rua dentro de um território."""
    
    _table = "ruas"
    _columns = ["id", "territorio_id", "nome"]
    
    def __init__(self, id: int = None, territorio_id: int = None, nome: str = ""):
        """
        Inicializa uma rua.
        
        Args:
            id (int, opcional): ID da rua.
            territorio_id (int, opcional): ID do território.
            nome (str, opcional): Nome da rua.
        """
        super().__init__(
            id=id,
            territorio_id=territorio_id,
            nome=nome
        )
        
        # Campos calculados ou relacionados que não estão diretamente na tabela
        self.territorio_nome = None
        self.total_imoveis = 0
        self.imoveis = []
    
    @classmethod
    def get_by_territorio(cls, db_manager, territorio_id: int) -> List['Rua']:
        """
        Obtém todas as ruas de um território.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            territorio_id (int): ID do território.
            
        Returns:
            List[Rua]: Lista de ruas do território.
        """
        return cls.get_all(db_manager, "territorio_id = ?", (territorio_id,), "nome")
    
    def get_imoveis(self, db_manager) -> List[Dict[str, Any]]:
        """
        Obtém todos os imóveis da rua.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            
        Returns:
            List[Dict[str, Any]]: Lista de imóveis da rua.
        """
        if self.id is not None:
            cursor = db_manager.execute(
                "SELECT * FROM imoveis WHERE rua_id = ? ORDER BY numero",
                (self.id,)
            )
            if cursor:
                return [dict(row) for row in cursor.fetchall()]
        return []
    
    def get_imoveis_por_tipo(self, db_manager, tipo: str) -> List[Dict[str, Any]]:
        """
        Obtém os imóveis da rua filtrados por tipo.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            tipo (str): Tipo de imóvel (residencial, comercial, predio, vila).
            
        Returns:
            List[Dict[str, Any]]: Lista de imóveis da rua do tipo especificado.
        """
        if self.id is not None:
            cursor = db_manager.execute(
                "SELECT * FROM imoveis WHERE rua_id = ? AND tipo = ? ORDER BY numero",
                (self.id, tipo)
            )
            if cursor:
                return [dict(row) for row in cursor.fetchall()]
        return []
    
    def add_imovel(self, db_manager, numero: str, tipo: str, 
                  nome: str = None, total_unidades: int = None) -> int:
        """
        Adiciona um novo imóvel à rua.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            numero (str): Número do imóvel.
            tipo (str): Tipo do imóvel (residencial, comercial, predio, vila).
            nome (str, opcional): Nome do imóvel (para prédios e vilas).
            total_unidades (int, opcional): Total de unidades (para prédios e vilas).
            
        Returns:
            int: ID do imóvel criado, ou None em caso de erro.
        """
        if self.id is not None:
            cursor = db_manager.execute(
                "INSERT INTO imoveis (rua_id, numero, tipo, nome, total_unidades) VALUES (?, ?, ?, ?, ?)",
                (self.id, numero, tipo, nome, total_unidades)
            )
            if cursor:
                db_manager.commit()
                return cursor.lastrowid
        return None
    
    def carregar_territorio_info(self, db_manager) -> bool:
        """
        Carrega informações do território ao qual a rua pertence.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            
        Returns:
            bool: True se as informações foram carregadas com sucesso, False caso contrário.
        """
        if self.territorio_id:
            cursor = db_manager.execute(
                "SELECT nome FROM territorios WHERE id = ?", 
                (self.territorio_id,)
            )
            if cursor:
                row = cursor.fetchone()
                if row:
                    self.territorio_nome = row['nome']
                    return True
        return False
    
    def contar_imoveis(self, db_manager) -> int:
        """
        Conta o número de imóveis na rua.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            
        Returns:
            int: Número de imóveis na rua.
        """
        if self.id is not None:
            cursor = db_manager.execute(
                "SELECT COUNT(*) as total FROM imoveis WHERE rua_id = ?",
                (self.id,)
            )
            if cursor:
                row = cursor.fetchone()
                if row:
                    self.total_imoveis = row['total']
                    return self.total_imoveis
        return 0
    
    def __str__(self) -> str:
        """
        Retorna uma representação em string da rua.
        
        Returns:
            str: Representação em string.
        """
        if self.territorio_nome:
            return f"{self.nome} ({self.territorio_nome})"
        return self.nome