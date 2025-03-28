#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
import sqlite3
import hashlib
import os
from models.base_model import BaseModel
from utils.validation import validate_required_fields

class Usuario(BaseModel):
    """Modelo para representar um usuário do sistema"""
    
    # Níveis de permissão
    NIVEL_ADMIN = 3     # Acesso total ao sistema
    NIVEL_GESTOR = 2    # Pode gerenciar territórios, designações, etc.
    NIVEL_BASICO = 1    # Apenas registra atendimentos e consulta dados
    
    def __init__(self, id: int = None, nome: str = "", email: str = "",
                 senha_hash: str = None, nivel_permissao: int = NIVEL_BASICO,
                 ativo: bool = True, data_criacao: str = None):
        super().__init__(id)
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.nivel_permissao = nivel_permissao
        self.ativo = ativo
        self.data_criacao = data_criacao
    
    @staticmethod
    def from_db_row(row: sqlite3.Row) -> 'Usuario':
        """Cria um objeto Usuario a partir de uma linha do banco de dados"""
        return Usuario(
            id=row['id'],
            nome=row['nome'],
            email=row['email'],
            senha_hash=row['senha_hash'],
            nivel_permissao=row['nivel_permissao'],
            ativo=bool(row['ativo']),
            data_criacao=row['data_criacao']
        )
    
    @staticmethod
    def get_all(db_manager) -> List['Usuario']:
        """Obtém todos os usuários do banco de dados"""
        cursor = db_manager.execute("SELECT * FROM usuarios ORDER BY nome")
        if cursor:
            return [Usuario.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_ativos(db_manager) -> List['Usuario']:
        """Obtém todos os usuários ativos do banco de dados"""
        cursor = db_manager.execute("SELECT * FROM usuarios WHERE ativo = 1 ORDER BY nome")
        if cursor:
            return [Usuario.from_db_row(row) for row in cursor.fetchall()]
        return []
    
    @staticmethod
    def get_by_id(db_manager, usuario_id: int) -> Optional['Usuario']:
        """Obtém um usuário pelo ID"""
        cursor = db_manager.execute(
            "SELECT * FROM usuarios WHERE id = ?", 
            (usuario_id,)
        )
        if cursor:
            row = cursor.fetchone()
            if row:
                return Usuario.from_db_row(row)
        return None
    
    @staticmethod
    def get_by_email(db_manager, email: str) -> Optional['Usuario']:
        """Obtém um usuário pelo email"""
        cursor = db_manager.execute(
            "SELECT * FROM usuarios WHERE email = ?", 
            (email,)
        )
        if cursor:
            row = cursor.fetchone()
            if row:
                return Usuario.from_db_row(row)
        return None
    
    @staticmethod
    def verificar_credenciais(db_manager, email: str, senha: str) -> Optional['Usuario']:
        """Verifica as credenciais de um usuário"""
        usuario = Usuario.get_by_email(db_manager, email)
        if usuario and usuario.verificar_senha(senha) and usuario.ativo:
            return usuario
        return None
    
    def definir_senha(self, senha: str) -> None:
        """Define a senha do usuário (faz o hash)"""
        # Gera um salt aleatório
        salt = os.urandom(32)
        # Gera o hash com o salt
        senha_hash = hashlib.pbkdf2_hmac(
            'sha256',
            senha.encode('utf-8'),
            salt,
            100000
        )
        # Armazena salt+hash
        self.senha_hash = salt.hex() + ":" + senha_hash.hex()
    
    def verificar_senha(self, senha: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        if not self.senha_hash:
            return False
        
        try:
            salt_str, hash_str = self.senha_hash.split(":")
            salt = bytes.fromhex(salt_str)
            hash_stored = bytes.fromhex(hash_str)
            
            # Calcula o hash da senha fornecida com o mesmo salt
            hash_senha = hashlib.pbkdf2_hmac(
                'sha256',
                senha.encode('utf-8'),
                salt,
                100000
            )
            
            return hash_senha == hash_stored
        except Exception:
            return False
    
    def validate(self) -> List[str]:
        """Valida os campos do usuário antes de salvar"""
        errors = []
        
        # Validar campos obrigatórios
        required_fields = [
            ('nome', 'Nome é obrigatório'),
            ('email', 'Email é obrigatório'),
            ('nivel_permissao', 'Nível de permissão é obrigatório')
        ]
        errors.extend(validate_required_fields(self, required_fields))
        
        # Validar formato de email (simplificado)
        if self.email and '@' not in self.email:
            errors.append("Email inválido")
        
        # Validar nível de permissão
        if (self.nivel_permissao is not None and 
            self.nivel_permissao not in [self.NIVEL_BASICO, self.NIVEL_GESTOR, self.NIVEL_ADMIN]):
            errors.append("Nível de permissão inválido")
        
        # Validar senha para novos usuários
        if self.id is None and not self.senha_hash:
            errors.append("Senha é obrigatória para novos usuários")
        
        return errors
    
    def save(self, db_manager) -> bool:
        """Salva o usuário no banco de dados"""
        # Validar antes de salvar
        errors = self.validate()
        if errors:
            print(f"Erro ao salvar usuário: {', '.join(errors)}")
            return False
            
        if self.id is None:
            # Verificar se o email já existe
            if Usuario.get_by_email(db_manager, self.email):
                print("Erro: Email já existe")
                return False
                
            # Inserir novo usuário
            cursor = db_manager.execute(
                "INSERT INTO usuarios (nome, email, senha_hash, nivel_permissao, ativo) "
                "VALUES (?, ?, ?, ?, ?)",
                (self.nome, self.email, self.senha_hash, self.nivel_permissao, int(self.ativo))
            )
            if cursor:
                self.id = cursor.lastrowid
                db_manager.commit()
                return True
        else:
            # Verificar se o email já existe para outro usuário
            existing = Usuario.get_by_email(db_manager, self.email)
            if existing and existing.id != self.id:
                print("Erro: Email já existe para outro usuário")
                return False
                
            # Atualizar usuário existente
            cursor = db_manager.execute(
                "UPDATE usuarios SET nome = ?, email = ?, senha_hash = ?, "
                "nivel_permissao = ?, ativo = ? WHERE id = ?",
                (self.nome, self.email, self.senha_hash, self.nivel_permissao, 
                 int(self.ativo), self.id)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def delete(self, db_manager) -> bool:
        """Deleta o usuário do banco de dados"""
        if self.id is not None:
            cursor = db_manager.execute(
                "DELETE FROM usuarios WHERE id = ?",
                (self.id,)
            )
            if cursor:
                db_manager.commit()
                return True
        return False
    
    def __str__(self) -> str:
        return f"{self.nome} ({self.email})"