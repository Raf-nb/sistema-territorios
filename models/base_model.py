#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe base para os modelos do sistema.
Fornece funcionalidades comuns para todos os modelos.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional, Type, TypeVar, ClassVar

# Tipo genérico para métodos de classe que retornam instâncias da própria classe
T = TypeVar('T', bound='BaseModel')

class BaseModel:
    """Classe base para todos os modelos de dados do sistema."""
    
    # Tabela associada ao modelo (deve ser sobrescrita por classes filhas)
    _table: ClassVar[str] = ""
    
    # Colunas principais da tabela (deve ser sobrescrita por classes filhas)
    _columns: ClassVar[List[str]] = []
    
    # Coluna de chave primária
    _primary_key: ClassVar[str] = "id"
    
    def __init__(self, **kwargs):
        """
        Inicializa um modelo com os atributos fornecidos.
        
        Args:
            **kwargs: Atributos do modelo.
        """
        # Inicializa atributos com valores padrão
        self.id = None
        self.data_criacao = None
        
        # Define os atributos passados como argumentos
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def from_db_row(cls: Type[T], row: sqlite3.Row) -> T:
        """
        Cria uma instância do modelo a partir de uma linha do banco de dados.
        
        Args:
            row (sqlite3.Row): Linha do banco de dados.
            
        Returns:
            T: Instância do modelo.
        """
        # Converter a linha para um dicionário e criar o objeto
        return cls(**{key: row[key] for key in row.keys() if hasattr(cls, key)})
    
    @classmethod
    def get_by_id(cls: Type[T], db_manager, model_id: int) -> Optional[T]:
        """
        Obtém um modelo pelo ID.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            model_id (int): ID do modelo a ser buscado.
            
        Returns:
            Optional[T]: Instância do modelo ou None se não encontrado.
        """
        if not cls._table:
            raise ValueError(f"A classe {cls.__name__} deve definir o atributo _table")
        
        query = f"SELECT * FROM {cls._table} WHERE {cls._primary_key} = ?"
        cursor = db_manager.execute(query, (model_id,))
        
        if cursor:
            row = cursor.fetchone()
            if row:
                return cls.from_db_row(row)
        
        return None
    
    @classmethod
    def get_all(cls: Type[T], db_manager, where: str = None, params: tuple = None, 
                order_by: str = None, limit: int = None) -> List[T]:
        """
        Obtém todos os modelos do banco de dados, com filtros opcionais.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            where (str, opcional): Condição WHERE da query SQL.
            params (tuple, opcional): Parâmetros para a condição WHERE.
            order_by (str, opcional): Ordem dos resultados.
            limit (int, opcional): Limite de resultados.
            
        Returns:
            List[T]: Lista de instâncias do modelo.
        """
        if not cls._table:
            raise ValueError(f"A classe {cls.__name__} deve definir o atributo _table")
        
        query = f"SELECT * FROM {cls._table}"
        
        if where:
            query += f" WHERE {where}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor = db_manager.execute(query, params)
        
        if cursor:
            return [cls.from_db_row(row) for row in cursor.fetchall()]
        
        return []
    
    def save(self, db_manager) -> bool:
        """
        Salva o modelo no banco de dados (insere ou atualiza).
        
        Args:
            db_manager: Gerenciador de banco de dados.
            
        Returns:
            bool: True se a operação foi bem-sucedida, False caso contrário.
        """
        if not self.__class__._table:
            raise ValueError(f"A classe {self.__class__.__name__} deve definir o atributo _table")
        
        if not self.__class__._columns:
            raise ValueError(f"A classe {self.__class__.__name__} deve definir o atributo _columns")
        
        # Coletar os valores das colunas do modelo
        values = {}
        for column in self.__class__._columns:
            if hasattr(self, column):
                values[column] = getattr(self, column)
        
        # Remove a coluna de ID se for uma inserção
        if self.id is None:
            if self._primary_key in values:
                del values[self._primary_key]
            
            # Inserir novo registro
            columns = ", ".join(values.keys())
            placeholders = ", ".join(["?"] * len(values))
            
            query = f"INSERT INTO {self.__class__._table} ({columns}) VALUES ({placeholders})"
            
            cursor = db_manager.execute(query, tuple(values.values()))
            
            if cursor:
                self.id = cursor.lastrowid
                db_manager.commit()
                return True
        else:
            # Atualizar registro existente
            set_clause = ", ".join([f"{key} = ?" for key in values.keys()])
            
            query = f"UPDATE {self.__class__._table} SET {set_clause} WHERE {self._primary_key} = ?"
            
            params = tuple(values.values()) + (self.id,)
            
            cursor = db_manager.execute(query, params)
            
            if cursor:
                db_manager.commit()
                return True
        
        return False
    
    def delete(self, db_manager) -> bool:
        """
        Remove o modelo do banco de dados.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            
        Returns:
            bool: True se a operação foi bem-sucedida, False caso contrário.
        """
        if not self.__class__._table:
            raise ValueError(f"A classe {self.__class__.__name__} deve definir o atributo _table")
        
        if self.id is None:
            return False
        
        query = f"DELETE FROM {self.__class__._table} WHERE {self._primary_key} = ?"
        
        cursor = db_manager.execute(query, (self.id,))
        
        if cursor:
            db_manager.commit()
            return True
        
        return False
    
    @classmethod
    def count(cls, db_manager, where: str = None, params: tuple = None) -> int:
        """
        Conta o número de registros que atendem a determinada condição.
        
        Args:
            db_manager: Gerenciador de banco de dados.
            where (str, opcional): Condição WHERE da query SQL.
            params (tuple, opcional): Parâmetros para a condição WHERE.
            
        Returns:
            int: Número de registros.
        """
        if not cls._table:
            raise ValueError(f"A classe {cls.__name__} deve definir o atributo _table")
        
        query = f"SELECT COUNT(*) as count FROM {cls._table}"
        
        if where:
            query += f" WHERE {where}"
        
        cursor = db_manager.execute(query, params)
        
        if cursor:
            row = cursor.fetchone()
            if row:
                return row['count']
        
        return 0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o modelo para um dicionário.
        
        Returns:
            Dict[str, Any]: Dicionário com os atributos do modelo.
        """
        result = {}
        for column in self.__class__._columns:
            if hasattr(self, column):
                result[column] = getattr(self, column)
        
        return result
    
    def __str__(self) -> str:
        """
        Retorna uma representação em string do modelo.
        
        Returns:
            str: Representação em string.
        """
        if hasattr(self, 'nome'):
            return f"{self.__class__.__name__}(id={self.id}, nome={self.nome})"
        else:
            return f"{self.__class__.__name__}(id={self.id})"