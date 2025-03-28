#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional, Dict, Any
import sqlite3
from models.base_model import BaseModel
from utils.validation import validate_required_fields

class Unidade(BaseModel):
    """Modelo para representar uma unidade de um prédio ou vila"""
    
    def __init__(self, id: int = None, imovel_id: int = None,
                 numero: str = "", observacoes: str = None):
        super().__init__(id)
        self.imovel_id = imovel_id
        self.numero = numero
        self.observacoes = observacoes
    
    @staticmethod
    def from_db_row(row: sqlite3.Row) -> 'Unidade':
        """Cria um objeto Unidade a partir de uma linha do banco de dados"""
        return Unidade(
            id=row['id'],
            imovel_id=row['imovel_id'],
            numero=row['numero'],
            observacoes=row['observacoes']
        )
    
    @staticmethod
    def get_by_id(db_manager, unidade_id: int) -> Optional['Unidade']:
        """Obtém uma unidade pelo ID"""
        cursor = db_manager.execute(
            "SELECT * FROM unidades WHERE id = ?", 
            (unidade_id,)
        )
        if cursor:
            row = cursor.fetchone()
            if row:
                return Unidade.from_db_row(row)
        return None
    
    @staticmethod
    def get_by_imovel(db_manager, imovel_id: int) -> List['Unidade']:
        """Obtém todas as unidades de um imóvel"""
        cursor = db_manager.execute(
            "SELECT * FROM unidades WHERE imovel_id = ? ORDER BY numero",
            (imovel_id,)
        )
        if cursor:
            return [Unidade.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    def validate(self) -> List[str]:
        """Valida os campos da unidade antes de salvar"""
        errors = []
        
        # Validar campos obrigatórios
        required_fields = [
            ('imovel_id', 'Imóvel é obrigatório'),
            ('numero', 'Número da unidade é obrigatório')
        ]
        errors.extend(validate_required_fields(self, required_fields))
        
        return errors
    
    def save(self, db_manager) -> bool:
        """Salva a unidade no banco de dados"""
        # Validar antes de salvar
        errors = self.validate()
        if errors:
            print(f"Erro ao salvar unidade: {', '.join(errors)}")
            return False
            
        if self.id is None:
            # Inserir nova unidade
            cursor = db_manager.execute(
                "INSERT INTO unidades (imovel_id, numero, observacoes) VALUES (?, ?, ?)",
                (self.imovel_id, self.numero, self.observacoes)
            )
            if cursor:
                self.id = cursor.lastrowid
                db_manager.commit()
                return True
        else:
            # Atualizar unidade existente
            cursor = db_manager.execute(
                "UPDATE unidades SET imovel_id = ?, numero = ?, observacoes = ? WHERE id = ?",
                (self.imovel_id, self.numero, self.observacoes, self.id)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def delete(self, db_manager) -> bool:
        """Deleta a unidade do banco de dados"""
        if self.id is not None:
            cursor = db_manager.execute(
                "DELETE FROM unidades WHERE id = ?",
                (self.id,)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def __str__(self) -> str:
        return f"Unidade {self.numero}"