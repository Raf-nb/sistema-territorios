#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
import sqlite3
from models.base_model import BaseModel
from utils.validation import validate_required_fields

class DesignacaoPredioVila(BaseModel):
    """Modelo para representar uma designação específica de prédio/vila"""
    
    def __init__(self, id: int = None, imovel_id: int = None,
                 responsavel: str = "", saida_campo_id: int = None,
                 data_designacao: str = "", data_devolucao: str = None,
                 status: str = "ativo"):
        super().__init__(id)
        self.imovel_id = imovel_id
        self.responsavel = responsavel
        self.saida_campo_id = saida_campo_id
        self.data_designacao = data_designacao
        self.data_devolucao = data_devolucao
        self.status = status  # 'ativo', 'concluido'
        
        # Campos extras para exibição
        self.imovel_numero = None
        self.imovel_nome = None
        self.imovel_tipo = None
        self.saida_campo_nome = None
        self.rua_nome = None
        self.territorio_nome = None
    
    @staticmethod
    def from_db_row(row: sqlite3.Row) -> 'DesignacaoPredioVila':
        """Cria um objeto DesignacaoPredioVila a partir de uma linha do banco de dados"""
        designacao = DesignacaoPredioVila(
            id=row['id'],
            imovel_id=row['imovel_id'],
            responsavel=row['responsavel'],
            saida_campo_id=row['saida_campo_id'],
            data_designacao=row['data_designacao'],
            data_devolucao=row['data_devolucao'],
            status=row['status']
        )
        
        # Adiciona campos extras se estiverem disponíveis
        for campo in ['imovel_numero', 'imovel_nome', 'imovel_tipo', 'saida_campo_nome', 
                      'rua_nome', 'territorio_nome']:
            if campo in row.keys():
                setattr(designacao, campo, row[campo])
            
        return designacao
    
    @staticmethod
    def get_all(db_manager) -> List['DesignacaoPredioVila']:
        """Obtém todas as designações de prédios/vilas do banco de dados"""
        cursor = db_manager.execute(
            "SELECT d.*, i.numero as imovel_numero, i.nome as imovel_nome, i.tipo as imovel_tipo, "
            "s.nome as saida_campo_nome, r.nome as rua_nome, t.nome as territorio_nome "
            "FROM designacoes_predios_vilas d "
            "JOIN imoveis i ON d.imovel_id = i.id "
            "JOIN saidas_campo s ON d.saida_campo_id = s.id "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "ORDER BY d.data_designacao DESC"
        )
        if cursor:
            return [DesignacaoPredioVila.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_ativas(db_manager) -> List['DesignacaoPredioVila']:
        """Obtém as designações ativas de prédios/vilas"""
        cursor = db_manager.execute(
            "SELECT d.*, i.numero as imovel_numero, i.nome as imovel_nome, i.tipo as imovel_tipo, "
            "s.nome as saida_campo_nome, r.nome as rua_nome, t.nome as territorio_nome "
            "FROM designacoes_predios_vilas d "
            "JOIN imoveis i ON d.imovel_id = i.id "
            "JOIN saidas_campo s ON d.saida_campo_id = s.id "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "WHERE d.status = 'ativo' "
            "ORDER BY d.data_designacao DESC"
        )
        if cursor:
            return [DesignacaoPredioVila.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_by_id(db_manager, designacao_id: int) -> Optional['DesignacaoPredioVila']:
        """Obtém uma designação de prédio/vila pelo ID"""
        cursor = db_manager.execute(
            "SELECT d.*, i.numero as imovel_numero, i.nome as imovel_nome, i.tipo as imovel_tipo, "
            "s.nome as saida_campo_nome, r.nome as rua_nome, t.nome as territorio_nome "
            "FROM designacoes_predios_vilas d "
            "JOIN imoveis i ON d.imovel_id = i.id "
            "JOIN saidas_campo s ON d.saida_campo_id = s.id "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "WHERE d.id = ?",
            (designacao_id,)
        )
        if cursor:
            row = cursor.fetchone()
            if row:
                return DesignacaoPredioVila.from_db_row(row)
        return None
    
    @staticmethod
    def get_by_imovel(db_manager, imovel_id: int) -> Optional['DesignacaoPredioVila']:
        """Obtém a designação ativa de um prédio/vila específico"""
        cursor = db_manager.execute(
            "SELECT d.*, i.numero as imovel_numero, i.nome as imovel_nome, i.tipo as imovel_tipo, "
            "s.nome as saida_campo_nome, r.nome as rua_nome, t.nome as territorio_nome "
            "FROM designacoes_predios_vilas d "
            "JOIN imoveis i ON d.imovel_id = i.id "
            "JOIN saidas_campo s ON d.saida_campo_id = s.id "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "WHERE d.imovel_id = ? AND d.status = 'ativo'",
            (imovel_id,)
        )
        if cursor:
            row = cursor.fetchone()
            if row:
                return DesignacaoPredioVila.from_db_row(row)
        return None
    
    def validate(self) -> List[str]:
        """Valida os campos da designação antes de salvar"""
        errors = []
        
        # Validar campos obrigatórios
        required_fields = [
            ('imovel_id', 'Imóvel é obrigatório'),
            ('responsavel', 'Responsável é obrigatório'),
            ('saida_campo_id', 'Saída de campo é obrigatória'),
            ('data_designacao', 'Data de designação é obrigatória'),
            ('status', 'Status é obrigatório')
        ]
        errors.extend(validate_required_fields(self, required_fields))
        
        # Validar status
        if self.status not in ['ativo', 'concluido']:
            errors.append("Status deve ser 'ativo' ou 'concluido'")
        
        return errors
    
    def save(self, db_manager) -> bool:
        """Salva a designação no banco de dados"""
        # Validar antes de salvar
        errors = self.validate()
        if errors:
            print(f"Erro ao salvar designação de prédio/vila: {', '.join(errors)}")
            return False
            
        if self.id is None:
            # Inserir nova designação
            cursor = db_manager.execute(
                "INSERT INTO designacoes_predios_vilas (imovel_id, responsavel, saida_campo_id, "
                "data_designacao, data_devolucao, status) VALUES (?, ?, ?, ?, ?, ?)",
                (self.imovel_id, self.responsavel, self.saida_campo_id, 
                 self.data_designacao, self.data_devolucao, self.status)
            )
            if cursor:
                self.id = cursor.lastrowid
                db_manager.commit()
                return True
        else:
            # Atualizar designação existente
            cursor = db_manager.execute(
                "UPDATE designacoes_predios_vilas SET imovel_id = ?, responsavel = ?, "
                "saida_campo_id = ?, data_designacao = ?, data_devolucao = ?, status = ? "
                "WHERE id = ?",
                (self.imovel_id, self.responsavel, self.saida_campo_id,
                 self.data_designacao, self.data_devolucao, self.status, self.id)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def concluir(self, db_manager) -> bool:
        """Marca a designação como concluída"""
        if self.id is not None:
            self.status = "concluido"
            cursor = db_manager.execute(
                "UPDATE designacoes_predios_vilas SET status = 'concluido' WHERE id = ?",
                (self.id,)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def delete(self, db_manager) -> bool:
        """Deleta a designação do banco de dados"""
        if self.id is not None:
            cursor = db_manager.execute(
                "DELETE FROM designacoes_predios_vilas WHERE id = ?",
                (self.id,)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def __str__(self) -> str:
        nome_imovel = self.imovel_nome if self.imovel_nome else f"Nº {self.imovel_numero}"
        return f"Designação: {nome_imovel} ({self.imovel_tipo.capitalize() if self.imovel_tipo else 'Imóvel'})"