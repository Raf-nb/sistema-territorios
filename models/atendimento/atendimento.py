#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional, Dict, Any
import sqlite3
from datetime import datetime
from models.base_model import BaseModel
from utils.validation import validate_required_fields

class Atendimento(BaseModel):
    """Modelo para representar um atendimento"""
    
    def __init__(self, id: int = None, imovel_id: int = None, unidade_id: int = None,
                 data: str = "", resultado: str = None, observacoes: str = None,
                 data_registro: str = None):
        super().__init__(id)
        self.imovel_id = imovel_id
        self.unidade_id = unidade_id
        self.data = data
        self.resultado = resultado  # 'positivo', 'ocupante-ausente', 'recusou', 'visitado'
        self.observacoes = observacoes
        self.data_registro = data_registro
        
        # Campos extras para exibição
        self.imovel_numero = None
        self.imovel_tipo = None
        self.rua_nome = None
        self.territorio_nome = None
        self.unidade_numero = None
    
    @staticmethod
    def from_db_row(row: sqlite3.Row) -> 'Atendimento':
        """Cria um objeto Atendimento a partir de uma linha do banco de dados"""
        atendimento = Atendimento(
            id=row['id'],
            imovel_id=row['imovel_id'],
            unidade_id=row['unidade_id'],
            data=row['data'],
            resultado=row['resultado'],
            observacoes=row['observacoes'],
            data_registro=row['data_registro']
        )
        
        # Adiciona campos extras se estiverem disponíveis
        for campo in ['imovel_numero', 'imovel_tipo', 'rua_nome', 'territorio_nome', 'unidade_numero']:
            if campo in row.keys():
                setattr(atendimento, campo, row[campo])
            
        return atendimento
    
    @staticmethod
    def get_all(db_manager) -> List['Atendimento']:
        """Obtém todos os atendimentos do banco de dados"""
        cursor = db_manager.execute(
            "SELECT a.*, i.numero as imovel_numero, i.tipo as imovel_tipo, "
            "r.nome as rua_nome, t.nome as territorio_nome, "
            "u.numero as unidade_numero "
            "FROM atendimentos a "
            "JOIN imoveis i ON a.imovel_id = i.id "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "LEFT JOIN unidades u ON a.unidade_id = u.id "
            "ORDER BY a.data DESC"
        )
        if cursor:
            return [Atendimento.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_by_imovel(db_manager, imovel_id: int) -> List['Atendimento']:
        """Obtém todos os atendimentos de um imóvel"""
        cursor = db_manager.execute(
            "SELECT a.*, i.numero as imovel_numero, i.tipo as imovel_tipo, "
            "r.nome as rua_nome, t.nome as territorio_nome, "
            "u.numero as unidade_numero "
            "FROM atendimentos a "
            "JOIN imoveis i ON a.imovel_id = i.id "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "LEFT JOIN unidades u ON a.unidade_id = u.id "
            "WHERE a.imovel_id = ? "
            "ORDER BY a.data DESC",
            (imovel_id,)
        )
        if cursor:
            return [Atendimento.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_by_unidade(db_manager, unidade_id: int) -> List['Atendimento']:
        """Obtém todos os atendimentos de uma unidade"""
        cursor = db_manager.execute(
            "SELECT a.*, i.numero as imovel_numero, i.tipo as imovel_tipo, "
            "r.nome as rua_nome, t.nome as territorio_nome, "
            "u.numero as unidade_numero "
            "FROM atendimentos a "
            "JOIN imoveis i ON a.imovel_id = i.id "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "JOIN unidades u ON a.unidade_id = u.id "
            "WHERE a.unidade_id = ? "
            "ORDER BY a.data DESC",
            (unidade_id,)
        )
        if cursor:
            return [Atendimento.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_ultimos(db_manager, limit: int = 10) -> List['Atendimento']:
        """Obtém os últimos atendimentos registrados"""
        cursor = db_manager.execute(
            "SELECT a.*, i.numero as imovel_numero, i.tipo as imovel_tipo, "
            "r.nome as rua_nome, t.nome as territorio_nome, "
            "u.numero as unidade_numero "
            "FROM atendimentos a "
            "JOIN imoveis i ON a.imovel_id = i.id "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "LEFT JOIN unidades u ON a.unidade_id = u.id "
            "ORDER BY a.data_registro DESC "
            "LIMIT ?",
            (limit,)
        )
        if cursor:
            return [Atendimento.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_estatisticas(db_manager) -> Dict[str, Any]:
        """Obtém estatísticas sobre os atendimentos"""
        estatisticas = {
            'total': 0,
            'por_resultado': {},
            'por_tipo': {},
            'por_territorio': {}
        }
        
        # Total de atendimentos
        cursor = db_manager.execute("SELECT COUNT(*) as total FROM atendimentos")
        if cursor:
            row = cursor.fetchone()
            if row:
                estatisticas['total'] = row['total']
        
        # Atendimentos por resultado
        cursor = db_manager.execute(
            "SELECT resultado, COUNT(*) as total FROM atendimentos GROUP BY resultado"
        )
        if cursor:
            for row in cursor.fetchall():
                if row['resultado']:
                    estatisticas['por_resultado'][row['resultado']] = row['total']
        
        # Atendimentos por tipo de imóvel
        cursor = db_manager.execute(
            "SELECT i.tipo, COUNT(*) as total "
            "FROM atendimentos a "
            "JOIN imoveis i ON a.imovel_id = i.id "
            "GROUP BY i.tipo"
        )
        if cursor:
            for row in cursor.fetchall():
                estatisticas['por_tipo'][row['tipo']] = row['total']
        
        # Atendimentos por território
        cursor = db_manager.execute(
            "SELECT t.nome, COUNT(*) as total "
            "FROM atendimentos a "
            "JOIN imoveis i ON a.imovel_id = i.id "
            "JOIN ruas r ON i.rua_id = r.id "
            "JOIN territorios t ON r.territorio_id = t.id "
            "GROUP BY t.id"
        )
        if cursor:
            for row in cursor.fetchall():
                estatisticas['por_territorio'][row['nome']] = row['total']
        
        return estatisticas
    
    def validate(self) -> List[str]:
        """Valida os campos do atendimento antes de salvar"""
        errors = []
        
        # Validar campos obrigatórios
        required_fields = [
            ('imovel_id', 'Imóvel é obrigatório'),
            ('data', 'Data é obrigatória')
        ]
        errors.extend(validate_required_fields(self, required_fields))
        
        # Validar resultado se fornecido
        resultados_validos = ['positivo', 'ocupante-ausente', 'recusou-atendimento', 'visitado']
        if self.resultado and self.resultado not in resultados_validos:
            errors.append(f"Resultado deve ser um dos seguintes: {', '.join(resultados_validos)}")
        
        return errors
    
    def save(self, db_manager) -> bool:
        """Salva o atendimento no banco de dados"""
        # Validar antes de salvar
        errors = self.validate()
        if errors:
            print(f"Erro ao salvar atendimento: {', '.join(errors)}")
            return False
            
        if self.id is None:
            # Inserir novo atendimento
            cursor = db_manager.execute(
                "INSERT INTO atendimentos (imovel_id, unidade_id, data, resultado, observacoes) "
                "VALUES (?, ?, ?, ?, ?)",
                (self.imovel_id, self.unidade_id, self.data, self.resultado, self.observacoes)
            )
            if cursor:
                self.id = cursor.lastrowid
                db_manager.commit()
                return True
        else:
            # Atualizar atendimento existente
            cursor = db_manager.execute(
                "UPDATE atendimentos SET imovel_id = ?, unidade_id = ?, data = ?, "
                "resultado = ?, observacoes = ? WHERE id = ?",
                (self.imovel_id, self.unidade_id, self.data, self.resultado, 
                 self.observacoes, self.id)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def delete(self, db_manager) -> bool:
        """Deleta o atendimento do banco de dados"""
        if self.id is not None:
            cursor = db_manager.execute(
                "DELETE FROM atendimentos WHERE id = ?",
                (self.id,)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def __str__(self) -> str:
        unidade = f" - {self.unidade_numero}" if self.unidade_numero else ""
        return f"Atendimento {self.data}: {self.imovel_numero}{unidade}"