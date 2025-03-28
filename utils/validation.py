#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários para validação de dados.
"""

import re
from typing import Dict, List, Any, Optional, Callable

def validate_required(value: Any, field_name: str) -> Optional[str]:
    """
    Valida se um campo obrigatório está preenchido.
    
    Args:
        value (Any): Valor do campo.
        field_name (str): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return f"O campo {field_name} é obrigatório."
    return None

def validate_min_length(value: str, min_length: int, field_name: str) -> Optional[str]:
    """
    Valida o tamanho mínimo de uma string.
    
    Args:
        value (str): Valor do campo.
        min_length (int): Tamanho mínimo.
        field_name (str): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if not value or len(value) < min_length:
        return f"O campo {field_name} deve ter pelo menos {min_length} caracteres."
    return None

def validate_max_length(value: str, max_length: int, field_name: str) -> Optional[str]:
    """
    Valida o tamanho máximo de uma string.
    
    Args:
        value (str): Valor do campo.
        max_length (int): Tamanho máximo.
        field_name (str): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if value and len(value) > max_length:
        return f"O campo {field_name} deve ter no máximo {max_length} caracteres."
    return None

def validate_email(value: str, field_name: str = "Email") -> Optional[str]:
    """
    Valida um endereço de email.
    
    Args:
        value (str): Valor do campo.
        field_name (str, opcional): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if not value:
        return None  # Não validar se vazio (usar validate_required para isso)
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        return f"O {field_name} informado não é válido."
    return None

def validate_numeric(value: str, field_name: str) -> Optional[str]:
    """
    Valida se um campo contém apenas números.
    
    Args:
        value (str): Valor do campo.
        field_name (str): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if not value:
        return None  # Não validar se vazio (usar validate_required para isso)
    
    if not value.isdigit():
        return f"O campo {field_name} deve conter apenas números."
    return None

def validate_date(value: str, field_name: str) -> Optional[str]:
    """
    Valida se um campo é uma data válida no formato YYYY-MM-DD.
    
    Args:
        value (str): Valor do campo.
        field_name (str): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if not value:
        return None  # Não validar se vazio (usar validate_required para isso)
    
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, value):
        return f"O campo {field_name} deve estar no formato YYYY-MM-DD."
    
    # Verificar se é uma data válida
    try:
        from datetime import datetime
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return f"O campo {field_name} contém uma data inválida."
    return None

def validate_phone(value: str, field_name: str = "Telefone") -> Optional[str]:
    """
    Valida um número de telefone.
    
    Args:
        value (str): Valor do campo.
        field_name (str, opcional): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if not value:
        return None  # Não validar se vazio (usar validate_required para isso)
    
    # Remover caracteres não numéricos
    digits = re.sub(r'\D', '', value)
    
    # Verificar o comprimento
    if len(digits) < 8 or len(digits) > 15:
        return f"O {field_name} informado não é válido."
    return None

def validate_select(value: Any, options: List[Any], field_name: str) -> Optional[str]:
    """
    Valida se um valor está entre as opções válidas.
    
    Args:
        value (Any): Valor do campo.
        options (List[Any]): Lista de opções válidas.
        field_name (str): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if value is None:
        return None  # Não validar se None (usar validate_required para isso)
    
    if value not in options:
        return f"O valor selecionado para {field_name} não é válido."
    return None

def validate_min_value(value: float, min_value: float, field_name: str) -> Optional[str]:
    """
    Valida o valor mínimo de um número.
    
    Args:
        value (float): Valor do campo.
        min_value (float): Valor mínimo.
        field_name (str): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if value is None:
        return None  # Não validar se None (usar validate_required para isso)
    
    if value < min_value:
        return f"O campo {field_name} deve ser maior ou igual a {min_value}."
    return None

def validate_max_value(value: float, max_value: float, field_name: str) -> Optional[str]:
    """
    Valida o valor máximo de um número.
    
    Args:
        value (float): Valor do campo.
        max_value (float): Valor máximo.
        field_name (str): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if value is None:
        return None  # Não validar se None (usar validate_required para isso)
    
    if value > max_value:
        return f"O campo {field_name} deve ser menor ou igual a {max_value}."
    return None

def validate_regex(value: str, pattern: str, field_name: str, message: Optional[str] = None) -> Optional[str]:
    """
    Valida se um campo corresponde a um padrão regex.
    
    Args:
        value (str): Valor do campo.
        pattern (str): Padrão regex.
        field_name (str): Nome do campo para mensagem de erro.
        message (str, opcional): Mensagem de erro personalizada.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if not value:
        return None  # Não validar se vazio (usar validate_required para isso)
    
    if not re.match(pattern, value):
        if message:
            return message
        return f"O campo {field_name} não está no formato correto."
    return None

def validate_password_strength(value: str, field_name: str = "Senha") -> Optional[str]:
    """
    Valida a força de uma senha.
    
    Args:
        value (str): Valor do campo.
        field_name (str, opcional): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if not value:
        return None  # Não validar se vazio (usar validate_required para isso)
    
    errors = []
    
    if len(value) < 8:
        errors.append("ter pelo menos 8 caracteres")
    
    if not re.search(r'[A-Z]', value):
        errors.append("conter pelo menos uma letra maiúscula")
    
    if not re.search(r'[a-z]', value):
        errors.append("conter pelo menos uma letra minúscula")
    
    if not re.search(r'\d', value):
        errors.append("conter pelo menos um número")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        errors.append("conter pelo menos um caractere especial")
    
    if errors:
        return f"A {field_name} deve {', '.join(errors[:-1])}{' e ' if len(errors) > 1 else ''}{errors[-1]}."
    return None

def validate_passwords_match(password1: str, password2: str) -> Optional[str]:
    """
    Valida se duas senhas são iguais.
    
    Args:
        password1 (str): Primeira senha.
        password2 (str): Segunda senha (confirmação).
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if password1 != password2:
        return "As senhas não coincidem."
    return None

def validate_form(data: Dict[str, Any], validations: Dict[str, List[Callable]]) -> Dict[str, str]:
    """
    Valida um formulário completo.
    
    Args:
        data (Dict[str, Any]): Dados do formulário.
        validations (Dict[str, List[Callable]]): Validações para cada campo.
        
    Returns:
        Dict[str, str]: Dicionário com os erros de validação (chave: campo, valor: mensagem).
    """
    errors = {}
    
    for field_name, validators in validations.items():
        field_value = data.get(field_name)
        
        for validator in validators:
            error = validator(field_value)
            if error:
                errors[field_name] = error
                break
    
    return errors

def validate_unique(value: str, db_manager, table: str, column: str, 
                   field_name: str, exclude_id: Optional[int] = None) -> Optional[str]:
    """
    Valida se um valor é único em uma tabela.
    
    Args:
        value (str): Valor do campo.
        db_manager: Gerenciador de banco de dados.
        table (str): Nome da tabela.
        column (str): Nome da coluna.
        field_name (str): Nome do campo para mensagem de erro.
        exclude_id (int, opcional): ID a excluir da validação (para edição).
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if not value:
        return None  # Não validar se vazio (usar validate_required para isso)
    
    query = f"SELECT COUNT(*) as count FROM {table} WHERE {column} = ?"
    params = [value]
    
    if exclude_id is not None:
        query += " AND id != ?"
        params.append(exclude_id)
    
    cursor = db_manager.execute(query, tuple(params))
    
    if cursor:
        row = cursor.fetchone()
        if row and row['count'] > 0:
            return f"O {field_name} informado já está em uso."
    
    return None

def validate_integer(value: Any, field_name: str) -> Optional[str]:
    """
    Valida se um valor é um número inteiro.
    
    Args:
        value (Any): Valor do campo.
        field_name (str): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if value is None:
        return None  # Não validar se None (usar validate_required para isso)
    
    try:
        int(value)
        return None
    except (ValueError, TypeError):
        return f"O campo {field_name} deve ser um número inteiro."

def validate_float(value: Any, field_name: str) -> Optional[str]:
    """
    Valida se um valor é um número decimal.
    
    Args:
        value (Any): Valor do campo.
        field_name (str): Nome do campo para mensagem de erro.
        
    Returns:
        Optional[str]: Mensagem de erro ou None se válido.
    """
    if value is None:
        return None  # Não validar se None (usar validate_required para isso)
    
    try:
        float(value)
        return None
    except (ValueError, TypeError):
        return f"O campo {field_name} deve ser um número decimal."