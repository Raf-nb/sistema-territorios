#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
from typing import List, Dict, Tuple, Optional

class SchemaValidator:
    """Classe para validar o esquema do banco de dados"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def validate_schema(self) -> Tuple[bool, List[str]]:
        """
        Valida se o banco de dados tem o esquema correto
        Retorna: (válido, lista de problemas)
        """
        problemas = []
        
        # Tabelas esperadas e suas colunas
        expected_tables = self._get_expected_tables()
        
        # Verificar tabelas existentes
        existing_tables = self._get_existing_tables()
        
        # Verificar tabelas ausentes
        missing_tables = set(expected_tables.keys()) - set(existing_tables)
        if missing_tables:
            problemas.append(f"Tabelas ausentes: {', '.join(missing_tables)}")
        
        # Para cada tabela existente, verificar colunas
        for table_name in set(expected_tables.keys()) & set(existing_tables):
            # Verificar colunas
            existing_columns = self._get_table_columns(table_name)
            expected_columns = expected_tables[table_name]
            
            # Verificar colunas ausentes
            expected_column_names = [col[0] for col in expected_columns]
            existing_column_names = [col[0] for col in existing_columns]
            
            missing_columns = set(expected_column_names) - set(existing_column_names)
            if missing_columns:
                problemas.append(f"Tabela '{table_name}': colunas ausentes: {', '.join(missing_columns)}")
        
        # Verificar se o banco de dados tem índices adequados
        for table_name in existing_tables:
            expected_indices = self._get_expected_indices(table_name)
            existing_indices = self._get_table_indices(table_name)
            
            missing_indices = [idx for idx in expected_indices if idx not in existing_indices]
            if missing_indices:
                problemas.append(f"Tabela '{table_name}': índices ausentes: {missing_indices}")
        
        # O esquema é válido se não houver problemas
        is_valid = len(problemas) == 0
        
        return (is_valid, problemas)
    
    def fix_schema_issues(self) -> Tuple[bool, List[str]]:
        """
        Tenta corrigir problemas de esquema no banco de dados
        Retorna: (sucesso, lista de ações realizadas)
        """
        acoes = []
        is_valid, problemas = self.validate_schema()
        
        if is_valid:
            acoes.append("O esquema do banco de dados já está correto, nenhuma ação necessária.")
            return (True, acoes)
        
        # Ler arquivos de esquema
        schema_files = [
            'schema_base.sql',
            'schema_usuarios.sql',
            'schema_relatorios.sql'
        ]
        
        # Executar cada arquivo de esquema
        for schema_file in schema_files:
            file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                'migrations', 
                schema_file
            )
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                
                # Executar o schema no banco de dados
                self.db_manager.execute(schema_sql)
                self.db_manager.commit()
                acoes.append(f"Executado arquivo de esquema: {schema_file}")
            except Exception as e:
                acoes.append(f"Erro ao executar {schema_file}: {str(e)}")
                return (False, acoes)
        
        # Verificar se os problemas foram resolvidos
        is_valid_now, problemas_restantes = self.validate_schema()
        
        if is_valid_now:
            acoes.append("Todos os problemas de esquema foram corrigidos com sucesso.")
            return (True, acoes)
        else:
            acoes.append("Alguns problemas de esquema persistem após a tentativa de correção:")
            acoes.extend([f"- {p}" for p in problemas_restantes])
            return (False, acoes)
    
    def _get_existing_tables(self) -> List[str]:
        """Obtém a lista de tabelas existentes no banco de dados"""
        cursor = self.db_manager.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        if cursor:
            return [row['name'] for row in cursor.fetchall()]
        return []
    
    def _get_table_columns(self, table_name: str) -> List[Tuple[str, str]]:
        """Obtém as colunas de uma tabela"""
        cursor = self.db_manager.execute(f"PRAGMA table_info({table_name})")
        if cursor:
            # Retorna uma lista de tuplas (nome, tipo)
            return [(row['name'], row['type']) for row in cursor.fetchall()]
        return []
    
    def _get_table_indices(self, table_name: str) -> List[str]:
        """Obtém os índices de uma tabela"""
        cursor = self.db_manager.execute(
            f"SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='{table_name}'"
        )
        if cursor:
            return [row['name'] for row in cursor.fetchall()]
        return []
    
    def _get_expected_tables(self) -> Dict[str, List[Tuple[str, str]]]:
        """
        Retorna um dicionário com as tabelas esperadas e suas colunas
        Formato: {nome_tabela: [(nome_coluna, tipo_coluna), ...]}
        """
        return {
            "territorios": [
                ("id", "INTEGER"), ("nome", "TEXT"), ("descricao", "TEXT"),
                ("ultima_visita", "TEXT"), ("data_criacao", "TEXT")
            ],
            "ruas": [
                ("id", "INTEGER"), ("territorio_id", "INTEGER"), ("nome", "TEXT")
            ],
            "imoveis": [
                ("id", "INTEGER"), ("rua_id", "INTEGER"), ("numero", "TEXT"),
                ("tipo", "TEXT"), ("nome", "TEXT"), ("total_unidades", "INTEGER"),
                ("tipo_portaria", "TEXT"), ("tipo_acesso", "TEXT"), ("observacoes", "TEXT")
            ],
            "unidades": [
                ("id", "INTEGER"), ("imovel_id", "INTEGER"), ("numero", "TEXT"),
                ("observacoes", "TEXT")
            ],
            "saidas_campo": [
                ("id", "INTEGER"), ("nome", "TEXT"), ("data", "TEXT"),
                ("dia_semana", "TEXT"), ("horario", "TEXT"), ("dirigente", "TEXT"),
                ("data_criacao", "TEXT")
            ],
            "designacoes": [
                ("id", "INTEGER"), ("territorio_id", "INTEGER"), ("saida_campo_id", "INTEGER"),
                ("data_designacao", "TEXT"), ("data_devolucao", "TEXT"), 
                ("responsavel", "TEXT"), ("status", "TEXT")
            ],
            "atendimentos": [
                ("id", "INTEGER"), ("imovel_id", "INTEGER"), ("unidade_id", "INTEGER"),
                ("data", "TEXT"), ("resultado", "TEXT"), ("observacoes", "TEXT"),
                ("data_registro", "TEXT")
            ],
            "historico_predios_vilas": [
                ("id", "INTEGER"), ("imovel_id", "INTEGER"), ("data", "TEXT"),
                ("descricao", "TEXT"), ("data_registro", "TEXT")
            ],
            "designacoes_predios_vilas": [
                ("id", "INTEGER"), ("imovel_id", "INTEGER"), ("responsavel", "TEXT"),
                ("saida_campo_id", "INTEGER"), ("data_designacao", "TEXT"),
                ("data_devolucao", "TEXT"), ("status", "TEXT")
            ],
            "usuarios": [
                ("id", "INTEGER"), ("nome", "TEXT"), ("email", "TEXT"),
                ("senha_hash", "TEXT"), ("nivel_permissao", "INTEGER"), 
                ("ativo", "INTEGER"), ("data_criacao", "TEXT")
            ],
            "log_atividades": [
                ("id", "INTEGER"), ("usuario_id", "INTEGER"), ("tipo_acao", "TEXT"),
                ("descricao", "TEXT"), ("data_hora", "TEXT"), ("entidade", "TEXT"),
                ("entidade_id", "INTEGER")
            ],
            "notificacoes": [
                ("id", "INTEGER"), ("usuario_id", "INTEGER"), ("tipo", "TEXT"),
                ("titulo", "TEXT"), ("mensagem", "TEXT"), ("status", "TEXT"),
                ("data_criacao", "TEXT"), ("data_leitura", "TEXT"), ("link", "TEXT"),
                ("entidade", "TEXT"), ("entidade_id", "INTEGER")
            ],
            "relatorios": [
                ("id", "INTEGER"), ("nome", "TEXT"), ("tipo", "TEXT"),
                ("filtros", "TEXT"), ("usuario_id", "INTEGER"), ("data_criacao", "TEXT"),
                ("ultima_execucao", "TEXT")
            ]
        }
    
    def _get_expected_indices(self, table_name: str) -> List[str]:
        """Retorna uma lista de índices esperados para uma tabela específica"""
        # Mapeamento de tabelas para índices esperados
        indices_map = {
            "usuarios": ["idx_usuarios_email"],
            "log_atividades": ["idx_log_usuario_id", "idx_log_data_hora"],
            "notificacoes": ["idx_notificacoes_usuario_id", "idx_notificacoes_status"],
            "ruas": ["idx_ruas_territorio_id"],
            "imoveis": ["idx_imoveis_rua_id"],
            "unidades": ["idx_unidades_imovel_id"],
            "designacoes": ["idx_designacoes_territorio_id", "idx_designacoes_saida_campo_id"],
            "atendimentos": ["idx_atendimentos_imovel_id"],
            "historico_predios_vilas": ["idx_historico_imovel_id"],
            "designacoes_predios_vilas": ["idx_designacoes_predios_vilas_imovel_id"],
            "relatorios": ["idx_relatorios_usuario_id", "idx_relatorios_tipo", "idx_relatorios_ultima_execucao"]
        }
        
        # Retornar índices para a tabela especificada ou lista vazia se não definido
        return indices_map.get(table_name, [])