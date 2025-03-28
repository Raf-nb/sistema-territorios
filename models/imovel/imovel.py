#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional, Dict, Any
import sqlite3
from models.base_model import BaseModel
from utils.validation import validate_required_fields

class Imovel(BaseModel):
    """Modelo para representar um imóvel"""
    
    def __init__(self, id: int = None, rua_id: int = None, 
                 numero: str = "", tipo: str = "", nome: str = None,
                 total_unidades: int = None, tipo_portaria: str = None,
                 tipo_acesso: str = None, observacoes: str = None):
        super().__init__(id)
        self.rua_id = rua_id
        self.numero = numero
        self.tipo = tipo  # 'residencial', 'comercial', 'predio', 'vila'
        self.nome = nome
        self.total_unidades = total_unidades
        self.tipo_portaria = tipo_portaria
        self.tipo_acesso = tipo_acesso
        self.observacoes = observacoes
        # Campos adicionais para join
        self.rua_nome = None
        self.territorio_nome = None
    
    @staticmethod
    def from_db_row(row: sqlite3.Row) -> 'Imovel':
        """Cria um objeto Imovel a partir de uma linha do banco de dados"""
        imovel = Imovel(
            id=row['id'],
            rua_id=row['rua_id'],
            numero=row['numero'],
            tipo=row['tipo'],
            nome=row['nome'],
            total_unidades=row['total_unidades'],
            tipo_portaria=row['tipo_portaria'],
            tipo_acesso=row['tipo_acesso'],
            observacoes=row['observacoes']
        )
        
        # Adiciona campos de join se estiverem disponíveis
        if 'rua_nome' in row.keys():
            imovel.rua_nome = row['rua_nome']
        if 'territorio_nome' in row.keys():
            imovel.territorio_nome = row['territorio_nome']
            
        return imovel
    
    @staticmethod
    def get_by_id(db_manager, imovel_id: int) -> Optional['Imovel']:
        """Obtém um imóvel pelo ID"""
        cursor = db_manager.execute(
            "SELECT i.*, r.nome as rua_nome, t.nome as territorio_nome "
            "FROM imoveis i "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "WHERE i.id = ?", 
            (imovel_id,)
        )
        if cursor:
            row = cursor.fetchone()
            if row:
                return Imovel.from_db_row(row)
        return None
    
    @staticmethod
    def get_by_rua(db_manager, rua_id: int) -> List['Imovel']:
        """Obtém todos os imóveis de uma rua"""
        cursor = db_manager.execute(
            "SELECT * FROM imoveis WHERE rua_id = ? ORDER BY numero",
            (rua_id,)
        )
        if cursor:
            return [Imovel.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_by_tipo(db_manager, tipo: str) -> List['Imovel']:
        """Obtém todos os imóveis de um determinado tipo"""
        cursor = db_manager.execute(
            "SELECT * FROM imoveis WHERE tipo = ? ORDER BY numero",
            (tipo,)
        )
        if cursor:
            return [Imovel.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_predios_vilas(db_manager) -> List['Imovel']:
        """Obtém todos os prédios e vilas"""
        cursor = db_manager.execute(
            "SELECT i.*, r.nome as rua_nome, t.nome as territorio_nome "
            "FROM imoveis i "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "WHERE i.tipo IN ('predio', 'vila') "
            "ORDER BY t.nome, r.nome, i.numero"
        )
        if cursor:
            return [Imovel.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    def validate(self) -> List[str]:
        """Valida os campos do imóvel antes de salvar"""
        errors = []
        
        # Validar campos obrigatórios
        required_fields = [
            ('rua_id', 'Rua é obrigatória'),
            ('numero', 'Número é obrigatório'),
            ('tipo', 'Tipo é obrigatório')
        ]
        errors.extend(validate_required_fields(self, required_fields))
        
        # Validar tipo
        tipos_validos = ['residencial', 'comercial', 'predio', 'vila']
        if self.tipo and self.tipo not in tipos_validos:
            errors.append(f"Tipo deve ser um dos seguintes: {', '.join(tipos_validos)}")
        
        # Para prédios e vilas, total_unidades é obrigatório
        if self.tipo in ['predio', 'vila'] and not self.total_unidades:
            errors.append("Total de unidades é obrigatório para prédios e vilas")
        
        return errors
    
    def save(self, db_manager) -> bool:
        """Salva o imóvel no banco de dados"""
        # Validar antes de salvar
        errors = self.validate()
        if errors:
            print(f"Erro ao salvar imóvel: {', '.join(errors)}")
            return False
            
        if self.id is None:
            # Inserir novo imóvel
            cursor = db_manager.execute(
                "INSERT INTO imoveis (rua_id, numero, tipo, nome, total_unidades, "
                "tipo_portaria, tipo_acesso, observacoes) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (self.rua_id, self.numero, self.tipo, self.nome, self.total_unidades,
                 self.tipo_portaria, self.tipo_acesso, self.observacoes)
            )
            if cursor:
                self.id = cursor.lastrowid
                db_manager.commit()
                
                # Se for prédio ou vila, criar unidades automaticamente
                if self.tipo in ('predio', 'vila') and self.total_unidades and self.total_unidades > 0:
                    self._criar_unidades(db_manager)
                
                return True
        else:
            # Atualizar imóvel existente
            cursor = db_manager.execute(
                "UPDATE imoveis SET rua_id = ?, numero = ?, tipo = ?, nome = ?, "
                "total_unidades = ?, tipo_portaria = ?, tipo_acesso = ?, observacoes = ? "
                "WHERE id = ?",
                (self.rua_id, self.numero, self.tipo, self.nome, self.total_unidades,
                 self.tipo_portaria, self.tipo_acesso, self.observacoes, self.id)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def _criar_unidades(self, db_manager) -> bool:
        """Cria as unidades para um prédio ou vila"""
        from models.imovel.unidade import Unidade
        
        if self.tipo == 'predio':
            # Para prédios, criar apartamentos numerados
            for i in range(1, self.total_unidades + 1):
                unidade = Unidade(
                    imovel_id=self.id,
                    numero=f"Apto {i:02d}"
                )
                unidade.save(db_manager)
        else:  # vila
            # Para vilas, criar casas numeradas
            for i in range(1, self.total_unidades + 1):
                unidade = Unidade(
                    imovel_id=self.id,
                    numero=f"Casa {i:02d}"
                )
                unidade.save(db_manager)
        
        return True
    
    def delete(self, db_manager) -> bool:
        """Deleta o imóvel do banco de dados"""
        if self.id is not None:
            cursor = db_manager.execute(
                "DELETE FROM imoveis WHERE id = ?",
                (self.id,)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def get_unidades(self, db_manager) -> List[Dict[str, Any]]:
        """Obtém todas as unidades do imóvel"""
        if self.id is not None:
            cursor = db_manager.execute(
                "SELECT * FROM unidades WHERE imovel_id = ? ORDER BY numero",
                (self.id,)
            )
            if cursor:
                return [dict(row) for row in cursor.fetchall()]
        return []
    
    def adicionar_historico(self, db_manager, data: str, descricao: str) -> bool:
        """Adiciona um registro ao histórico do prédio/vila"""
        if self.id is not None and self.tipo in ('predio', 'vila'):
            cursor = db_manager.execute(
                "INSERT INTO historico_predios_vilas (imovel_id, data, descricao) VALUES (?, ?, ?)",
                (self.id, data, descricao)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def get_historico(self, db_manager) -> List[Dict[str, Any]]:
        """Obtém o histórico do prédio/vila"""
        if self.id is not None and self.tipo in ('predio', 'vila'):
            cursor = db_manager.execute(
                "SELECT * FROM historico_predios_vilas WHERE imovel_id = ? ORDER BY data DESC",
                (self.id,)
            )
            if cursor:
                return [dict(row) for row in cursor.fetchall()]
        return []
    
    def __str__(self) -> str:
        return f"{self.numero} - {self.tipo.capitalize()}"