#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe responsável por gerenciar a conexão com o banco de dados.
"""

import os
import sqlite3
from datetime import datetime

from utils.config_reader import get_config

class DatabaseManager:
    """Gerenciador de banco de dados que fornece acesso ao SQLite."""
    
    def __init__(self, db_path=None):
        """
        Inicializa o gerenciador de banco de dados.
        
        Args:
            db_path (str, opcional): Caminho para o arquivo de banco de dados.
                Se não fornecido, usa o caminho das configurações.
        """
        config = get_config()
        self.db_path = db_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
            config['database']['path']
        )
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """
        Estabelece a conexão com o banco de dados.
        
        Returns:
            bool: True se a conexão foi estabelecida com sucesso, False caso contrário.
        """
        try:
            # Certifica-se de que o diretório do banco de dados existe
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Para acessar colunas pelo nome
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False
    
    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def commit(self):
        """
        Comita as alterações no banco de dados.
        """
        if self.connection:
            self.connection.commit()
    
    def execute(self, query, params=None):
        """
        Executa uma query SQL.
        
        Args:
            query (str): Query SQL a ser executada.
            params (tuple, opcional): Parâmetros para a query.
            
        Returns:
            sqlite3.Cursor: Cursor com os resultados da query, ou None em caso de erro.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            return None
    
    def executemany(self, query, params_list):
        """
        Executa uma query SQL múltiplas vezes com diferentes parâmetros.
        
        Args:
            query (str): Query SQL a ser executada.
            params_list (list): Lista de parâmetros para a query.
            
        Returns:
            sqlite3.Cursor: Cursor com os resultados da query, ou None em caso de erro.
        """
        try:
            self.cursor.executemany(query, params_list)
            return self.cursor
        except sqlite3.Error as e:
            print(f"Erro ao executar query múltipla: {e}")
            return None
    
    def executescript(self, script):
        """
        Executa um script SQL completo.
        
        Args:
            script (str): Script SQL a ser executado.
            
        Returns:
            bool: True se o script foi executado com sucesso, False caso contrário.
        """
        try:
            self.cursor.executescript(script)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao executar script: {e}")
            return False
    
    def setup_database(self):
        """
        Configura o banco de dados com os esquemas necessários.
        
        Returns:
            bool: True se o banco de dados foi configurado com sucesso, False caso contrário.
        """
        # Executa os arquivos de esquema em ordem
        schema_files = [
            'migrations/schema_base.sql', 
            'migrations/schema_usuarios.sql',
            'migrations/schema_relatorios.sql'
        ]
        
        for schema_file in schema_files:
            success = self._execute_schema_file(schema_file)
            if not success:
                return False
        
        # Verifica se precisa criar dados iniciais
        self._setup_initial_data()
        
        return True
    
    def _execute_schema_file(self, relative_path):
        """
        Executa um arquivo de esquema SQL.
        
        Args:
            relative_path (str): Caminho relativo para o arquivo SQL dentro do diretório database.
            
        Returns:
            bool: True se o esquema foi executado com sucesso, False caso contrário.
        """
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
        try:
            if not os.path.exists(schema_path):
                print(f"Arquivo de esquema não encontrado: {schema_path}")
                return False
                
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = f.read()
            
            return self.executescript(schema)
        except Exception as e:
            print(f"Erro ao executar arquivo de esquema {relative_path}: {e}")
            return False
    
    def _setup_initial_data(self):
        """
        Configura dados iniciais no banco de dados, se necessário.
        """
        # Verifica se há territórios
        cursor = self.execute("SELECT COUNT(*) FROM territorios")
        if cursor and cursor.fetchone()[0] == 0:
            self._criar_dados_exemplo()
        
        # Verifica se há usuários
        cursor = self.execute("SELECT COUNT(*) FROM usuarios")
        if cursor and cursor.fetchone()[0] == 0:
            self._criar_usuario_admin()
    
    def _criar_usuario_admin(self):
        """
        Cria o usuário administrador padrão.
        """
        try:
            # Importa o módulo Usuario aqui para evitar importação circular
            from core.constants import NivelPermissao
            
            print("Criando usuário administrador padrão...")
            
            # Gera um hash para a senha 'admin123'
            import hashlib
            import os
            
            salt = os.urandom(32)
            senha = 'admin123'
            senha_hash = hashlib.pbkdf2_hmac(
                'sha256',
                senha.encode('utf-8'),
                salt,
                100000
            )
            
            # Armazena salt+hash
            senha_hash_str = salt.hex() + ":" + senha_hash.hex()
            
            # Insere o usuário admin
            cursor = self.execute(
                "INSERT INTO usuarios (nome, email, senha_hash, nivel_permissao, ativo) "
                "VALUES (?, ?, ?, ?, ?)",
                ("Administrador", "admin@sistema.local", senha_hash_str, NivelPermissao.ADMIN, 1)
            )
            
            if cursor:
                self.commit()
                print("Usuário administrador criado com sucesso.")
            else:
                print("Erro ao criar usuário administrador.")
        except Exception as e:
            print(f"Erro ao criar usuário administrador: {e}")
    
    def _criar_dados_exemplo(self):
        """
        Cria dados de exemplo para o banco de dados.
        """
        print("Criando dados de exemplo...")
        
        # Cria alguns territórios de exemplo
        self.execute(
            "INSERT INTO territorios (nome, descricao) VALUES (?, ?)",
            ("Território 1", "Quadra 10 - Setor Central")
        )
        territorio_id = self.cursor.lastrowid
        
        # Cria algumas ruas para o território
        self.execute(
            "INSERT INTO ruas (territorio_id, nome) VALUES (?, ?)",
            (territorio_id, "Rua das Flores")
        )
        rua_id = self.cursor.lastrowid
        
        # Cria alguns imóveis para a rua
        imoveis = [
            (rua_id, "123", "residencial", None, None),
            (rua_id, "125", "comercial", None, None),
            (rua_id, "127", "predio", "Edifício Central", 12),
            (rua_id, "129", "vila", "Vila Aurora", 8)
        ]
        self.executemany(
            "INSERT INTO imoveis (rua_id, numero, tipo, nome, total_unidades) VALUES (?, ?, ?, ?, ?)",
            imoveis
        )
        
        # Cria saídas de campo
        saidas = [
            ("Saída 1", datetime.now().strftime('%Y-%m-%d'), "Terça-feira", "09:00", "João"),
            ("Saída 2", datetime.now().strftime('%Y-%m-%d'), "Quarta-feira", "19:30", "Maria"),
            ("Saída 3", datetime.now().strftime('%Y-%m-%d'), "Sexta-feira", "14:00", "Pedro")
        ]
        self.executemany(
            "INSERT INTO saidas_campo (nome, data, dia_semana, horario, dirigente) VALUES (?, ?, ?, ?, ?)",
            saidas
        )
        
        self.commit()
        print("Dados de exemplo criados com sucesso.")