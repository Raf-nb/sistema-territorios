#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários para manipulação de strings.
"""

import re
import unicodedata
from typing import List, Dict, Any, Optional

def normalize_string(text: str) -> str:
    """
    Normaliza uma string removendo acentos e convertendo para minúsculas.
    
    Args:
        text (str): Texto a ser normalizado.
        
    Returns:
        str: Texto normalizado.
    """
    if not text:
        return ""
    
    # Remover acentos
    normalized = unicodedata.normalize('NFKD', text)
    normalized = ''.join([c for c in normalized if not unicodedata.combining(c)])
    
    # Converter para minúsculas
    normalized = normalized.lower()
    
    return normalized

def text_to_slug(text: str) -> str:
    """
    Converte um texto para um slug (para URLs).
    
    Args:
        text (str): Texto a ser convertido.
        
    Returns:
        str: Slug gerado.
    """
    if not text:
        return ""
    
    # Normalizar
    slug = normalize_string(text)
    
    # Substituir espaços e caracteres não alfanuméricos por hífens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    
    # Remover hífens do início e do fim
    slug = slug.strip('-')
    
    return slug

def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Trunca uma string se ela exceder o tamanho máximo.
    
    Args:
        text (str): Texto a ser truncado.
        max_length (int): Tamanho máximo.
        suffix (str, opcional): Sufixo a ser adicionado quando truncado.
        
    Returns:
        str: Texto truncado.
    """
    if not text or len(text) <= max_length:
        return text
    
    # Truncar considerando o tamanho do sufixo
    return text[:max_length - len(suffix)] + suffix

def format_phone_number(phone: str) -> str:
    """
    Formata um número de telefone.
    
    Args:
        phone (str): Número de telefone.
        
    Returns:
        str: Número formatado.
    """
    if not phone:
        return ""
    
    # Remover caracteres não numéricos
    digits = re.sub(r'\D', '', phone)
    
    # Verificar o tamanho
    if len(digits) == 8:
        # Telefone fixo local 8 dígitos
        return f"{digits[:4]}-{digits[4:]}"
    elif len(digits) == 9:
        # Celular local 9 dígitos
        return f"{digits[:5]}-{digits[5:]}"
    elif len(digits) == 10:
        # Telefone fixo com DDD
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    elif len(digits) == 11:
        # Celular com DDD
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    elif len(digits) > 11:
        # Número com código internacional
        return f"+{digits[:2]} ({digits[2:4]}) {digits[4:9]}-{digits[9:13]}"
    else:
        # Retornar como está
        return phone

def format_currency(value: float, symbol: str = "R$", decimal_places: int = 2) -> str:
    """
    Formata um valor monetário.
    
    Args:
        value (float): Valor a ser formatado.
        symbol (str, opcional): Símbolo da moeda.
        decimal_places (int, opcional): Número de casas decimais.
        
    Returns:
        str: Valor formatado.
    """
    try:
        # Formatar o valor com separador de milhares e casas decimais
        formatted = f"{value:,.{decimal_places}f}"
        
        # Substituir vírgula por placeholder, ponto por vírgula e placeholder por ponto
        formatted = formatted.replace(',', 'COMMA').replace('.', ',').replace('COMMA', '.')
        
        # Adicionar símbolo da moeda
        if symbol:
            formatted = f"{symbol} {formatted}"
        
        return formatted
    except Exception:
        return f"{symbol} {value}"

def extract_initials(name: str, max_initials: int = 2) -> str:
    """
    Extrai as iniciais de um nome.
    
    Args:
        name (str): Nome completo.
        max_initials (int, opcional): Número máximo de iniciais.
        
    Returns:
        str: Iniciais do nome.
    """
    if not name:
        return ""
    
    # Dividir o nome em partes
    parts = name.split()
    
    # Remover preposições e artigos
    skip_words = ['de', 'da', 'do', 'das', 'dos', 'e']
    filtered_parts = [part for part in parts if part.lower() not in skip_words]
    
    # Caso não reste nenhuma parte após filtrar
    if not filtered_parts and parts:
        filtered_parts = parts
    
    # Obter iniciais
    initials = ""
    for i, part in enumerate(filtered_parts):
        if i >= max_initials:
            break
        if part:
            initials += part[0].upper()
    
    return initials

def is_valid_email(email: str) -> bool:
    """
    Verifica se um email é válido.
    
    Args:
        email (str): Email a ser verificado.
        
    Returns:
        bool: True se o email for válido, False caso contrário.
    """
    if not email:
        return False
    
    # Padrão de email simples
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def highlight_search_term(text: str, search_term: str, highlight_start: str = "<strong>", highlight_end: str = "</strong>") -> str:
    """
    Destaca um termo de busca em um texto.
    
    Args:
        text (str): Texto completo.
        search_term (str): Termo a ser destacado.
        highlight_start (str, opcional): Marcador de início do destaque.
        highlight_end (str, opcional): Marcador de fim do destaque.
        
    Returns:
        str: Texto com termo destacado.
    """
    if not text or not search_term:
        return text
    
    # Escapar caracteres especiais do termo de busca para regex
    escaped_term = re.escape(search_term)
    
    # Criar um padrão que ignora maiúsculas/minúsculas e acentos
    pattern = f"({escaped_term})"
    
    # Substituir todas as ocorrências
    return re.sub(pattern, f"{highlight_start}\\1{highlight_end}", text, flags=re.IGNORECASE)

def split_name(full_name: str) -> Dict[str, str]:
    """
    Divide um nome completo em primeiro nome e sobrenome.
    
    Args:
        full_name (str): Nome completo.
        
    Returns:
        Dict[str, str]: Dicionário com 'first_name' e 'last_name'.
    """
    if not full_name:
        return {'first_name': '', 'last_name': ''}
    
    parts = full_name.strip().split()
    
    if len(parts) == 1:
        return {'first_name': parts[0], 'last_name': ''}
    
    first_name = parts[0]
    last_name = ' '.join(parts[1:])
    
    return {'first_name': first_name, 'last_name': last_name}

def clean_html(html: str) -> str:
    """
    Remove tags HTML de um texto.
    
    Args:
        html (str): Texto com tags HTML.
        
    Returns:
        str: Texto sem tags HTML.
    """
    if not html:
        return ""
    
    # Remover tags HTML
    clean = re.sub(r'<[^>]+>', '', html)
    
    # Substituir entidades HTML comuns
    clean = clean.replace('&nbsp;', ' ')
    clean = clean.replace('&lt;', '<')
    clean = clean.replace('&gt;', '>')
    clean = clean.replace('&amp;', '&')
    clean = clean.replace('&quot;', '"')
    clean = clean.replace('&apos;', "'")
    
    # Remover espaços extras
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    return clean

def pluralize(singular: str, count: int, plural: Optional[str] = None) -> str:
    """
    Retorna a forma singular ou plural de uma palavra com base na contagem.
    
    Args:
        singular (str): Forma singular da palavra.
        count (int): Contagem.
        plural (str, opcional): Forma plural da palavra (se não seguir regra padrão).
        
    Returns:
        str: Forma singular ou plural baseada na contagem.
    """
    if count == 1:
        return singular
    
    if plural:
        return plural
    
    # Regras básicas de pluralização em português
    if singular.endswith(('r', 's', 'z')):
        return singular + 'es'
    elif singular.endswith('m'):
        return singular[:-1] + 'ns'
    elif singular.endswith('l'):
        if singular.endswith('il'):
            return singular[:-2] + 'is'
        return singular[:-1] + 'is'
    elif singular.endswith('ão'):
        return singular[:-2] + 'ões'
    else:
        return singular + 's'