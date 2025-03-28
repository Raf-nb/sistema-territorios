#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serviço de autenticação e gerenciamento de sessões.
"""

import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import uuid

from core.constants import NivelPermissao

class AuthService:
    """Serviço para autenticação e gerenciamento de sessões."""
    
    # Constantes para configuração
    DEFAULT_SESSION_TIMEOUT_MINUTES = 30
    DEFAULT_PASSWORD_ITERATIONS = 100000
    DEFAULT_TOKEN_BYTES = 32
    
    def __init__(self, db_manager):
        """
        Inicializa o serviço de autenticação.
        
        Args:
            db_manager: Gerenciador de banco de dados.
        """
        self.db_manager = db_manager
    
    def authenticate(self, email: str, senha: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Autentica um usuário pelo email e senha.
        
        Args:
            email (str): Email do usuário.
            senha (str): Senha do usuário.
            
        Returns:
            Tuple[bool, Optional[Dict[str, Any]]]: (sucesso, dados do usuário) ou (falha, None).
        """
        # Verificar se o usuário existe
        cursor = self.db_manager.execute(
            "SELECT * FROM usuarios WHERE email = ? AND ativo = 1",
            (email,)
        )
        
        if not cursor:
            return False, None
        
        usuario = cursor.fetchone()
        if not usuario:
            return False, None
        
        # Verificar a senha
        if not self._verificar_senha(senha, usuario['senha_hash']):
            return False, None
        
        # Atualizar última atividade
        self.db_manager.execute(
            "UPDATE usuarios SET ultima_atividade = CURRENT_TIMESTAMP WHERE id = ?",
            (usuario['id'],)
        )
        self.db_manager.commit()
        
        # Criar sessão
        token = self.criar_sessao(usuario['id'])
        
        # Registrar login
        self._registrar_login(usuario['id'])
        
        usuario_dict = dict(usuario)
        usuario_dict['token'] = token
        
        return True, usuario_dict
    
    def _verificar_senha(self, senha: str, senha_hash: str) -> bool:
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.
        
        Args:
            senha (str): Senha a ser verificada.
            senha_hash (str): Hash armazenado.
            
        Returns:
            bool: True se a senha estiver correta, False caso contrário.
        """
        try:
            # Formato do hash: salt_hex:hash_hex
            salt_str, hash_str = senha_hash.split(":")
            salt = bytes.fromhex(salt_str)
            hash_stored = bytes.fromhex(hash_str)
            
            # Calcular o hash da senha fornecida com o mesmo salt
            hash_senha = hashlib.pbkdf2_hmac(
                'sha256',
                senha.encode('utf-8'),
                salt,
                self.DEFAULT_PASSWORD_ITERATIONS
            )
            
            return hash_senha == hash_stored
        except Exception:
            return False
    
    def _registrar_login(self, usuario_id: int) -> bool:
        """
        Registra o login do usuário no log de atividades.
        
        Args:
            usuario_id (int): ID do usuário.
            
        Returns:
            bool: True se o registro foi bem-sucedido, False caso contrário.
        """
        cursor = self.db_manager.execute(
            "INSERT INTO log_atividades (usuario_id, tipo_acao, descricao) VALUES (?, ?, ?)",
            (usuario_id, "login", "Login realizado com sucesso")
        )
        
        if cursor:
            self.db_manager.commit()
            return True
        return False
    
    def criar_sessao(self, usuario_id: int, ip_address: str = None, 
                    user_agent: str = None, timeout_minutes: int = None) -> str:
        """
        Cria uma nova sessão para o usuário.
        
        Args:
            usuario_id (int): ID do usuário.
            ip_address (str, opcional): Endereço IP.
            user_agent (str, opcional): User-Agent do navegador.
            timeout_minutes (int, opcional): Tempo de expiração em minutos.
            
        Returns:
            str: Token de sessão.
        """
        # Gerar token único
        token = secrets.token_hex(self.DEFAULT_TOKEN_BYTES)
        
        # Calcular data de expiração
        if not timeout_minutes:
            timeout_minutes = self.DEFAULT_SESSION_TIMEOUT_MINUTES
        
        data_expiracao = (datetime.now() + timedelta(minutes=timeout_minutes)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Salvar a sessão no banco de dados
        cursor = self.db_manager.execute(
            "INSERT INTO sessoes (usuario_id, token, ip_address, user_agent, data_expiracao) "