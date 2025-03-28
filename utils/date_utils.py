#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários para manipulação de datas.
"""

import datetime
from typing import Optional, List, Tuple, Dict

def format_date(date_str: str, input_format: str = "%Y-%m-%d", output_format: str = "%d/%m/%Y") -> str:
    """
    Formata uma data de um formato para outro.
    
    Args:
        date_str (str): String de data.
        input_format (str, opcional): Formato de entrada.
        output_format (str, opcional): Formato de saída.
        
    Returns:
        str: Data formatada ou a string original se a conversão falhar.
    """
    if not date_str:
        return ""
    
    try:
        date_obj = datetime.datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except Exception:
        return date_str

def get_current_date(format: str = "%Y-%m-%d") -> str:
    """
    Obtém a data atual no formato especificado.
    
    Args:
        format (str, opcional): Formato de saída.
        
    Returns:
        str: Data atual formatada.
    """
    return datetime.datetime.now().strftime(format)

def get_date_diff_days(date_str1: str, date_str2: str, format: str = "%Y-%m-%d") -> int:
    """
    Calcula a diferença em dias entre duas datas.
    
    Args:
        date_str1 (str): Primeira data.
        date_str2 (str): Segunda data.
        format (str, opcional): Formato das datas.
        
    Returns:
        int: Diferença em dias ou 0 se houver erro.
    """
    try:
        date1 = datetime.datetime.strptime(date_str1, format).date()
        date2 = datetime.datetime.strptime(date_str2, format).date()
        return abs((date2 - date1).days)
    except Exception:
        return 0

def add_days(date_str: str, days: int, format: str = "%Y-%m-%d") -> str:
    """
    Adiciona dias a uma data.
    
    Args:
        date_str (str): Data inicial.
        days (int): Número de dias a adicionar (pode ser negativo).
        format (str, opcional): Formato da data.
        
    Returns:
        str: Nova data ou string vazia se houver erro.
    """
    try:
        date_obj = datetime.datetime.strptime(date_str, format).date()
        new_date = date_obj + datetime.timedelta(days=days)
        return new_date.strftime(format)
    except Exception:
        return ""

def get_date_weekday(date_str: str, format: str = "%Y-%m-%d") -> str:
    """
    Obtém o dia da semana de uma data.
    
    Args:
        date_str (str): Data.
        format (str, opcional): Formato da data.
        
    Returns:
        str: Nome do dia da semana em português ou string vazia se houver erro.
    """
    weekdays = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", 
                "Quinta-feira", "Sexta-feira", "Sábado"]
    
    try:
        date_obj = datetime.datetime.strptime(date_str, format).date()
        weekday_index = date_obj.weekday()
        # Ajusta para começar no domingo (0)
        weekday_index = (weekday_index + 1) % 7
        return weekdays[weekday_index]
    except Exception:
        return ""

def get_month_start_end(year: int, month: int) -> Tuple[str, str]:
    """
    Obtém o primeiro e último dia de um mês específico.
    
    Args:
        year (int): Ano.
        month (int): Mês (1-12).
        
    Returns:
        Tuple[str, str]: Datas de início e fim do mês no formato 'YYYY-MM-DD'.
    """
    try:
        # Primeiro dia do mês
        start_date = datetime.date(year, month, 1)
        
        # Último dia do mês (primeiro dia do próximo mês - 1 dia)
        if month == 12:
            end_date = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    except Exception:
        return "", ""

def get_current_month_start_end() -> Tuple[str, str]:
    """
    Obtém o primeiro e último dia do mês atual.
    
    Returns:
        Tuple[str, str]: Datas de início e fim do mês atual no formato 'YYYY-MM-DD'.
    """
    today = datetime.date.today()
    return get_month_start_end(today.year, today.month)

def get_month_name(month: int) -> str:
    """
    Obtém o nome do mês em português.
    
    Args:
        month (int): Número do mês (1-12).
        
    Returns:
        str: Nome do mês em português.
    """
    months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
              "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    if 1 <= month <= 12:
        return months[month - 1]
    return ""

def get_last_months(num_months: int) -> List[Dict[str, str]]:
    """
    Obtém uma lista dos últimos meses.
    
    Args:
        num_months (int): Número de meses a retornar.
        
    Returns:
        List[Dict[str, str]]: Lista de dicionários com informações dos meses.
            Cada dicionário contém 'year', 'month', 'name', 'start_date', 'end_date'.
    """
    today = datetime.date.today()
    year = today.year
    month = today.month
    
    result = []
    
    for i in range(num_months):
        # Calcular mês e ano (retrocedendo)
        if month <= 0:
            month = 12
            year -= 1
        
        start_date, end_date = get_month_start_end(year, month)
        
        result.append({
            'year': year,
            'month': month,
            'name': f"{get_month_name(month)}/{year}",
            'start_date': start_date,
            'end_date': end_date
        })
        
        month -= 1
    
    return result

def is_valid_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
    """
    Verifica se uma string representa uma data válida.
    
    Args:
        date_str (str): String de data.
        format (str, opcional): Formato da data.
        
    Returns:
        bool: True se a data for válida, False caso contrário.
    """
    try:
        datetime.datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def get_age_from_date(date_str: str, format: str = "%Y-%m-%d") -> int:
    """
    Calcula a idade a partir de uma data de nascimento.
    
    Args:
        date_str (str): Data de nascimento.
        format (str, opcional): Formato da data.
        
    Returns:
        int: Idade em anos ou -1 se houver erro.
    """
    try:
        birth_date = datetime.datetime.strptime(date_str, format).date()
        today = datetime.date.today()
        
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except Exception:
        return -1

def get_date_period_description(date_str: str, format: str = "%Y-%m-%d") -> str:
    """
    Retorna uma descrição relativa ao período de uma data (hoje, ontem, amanhã, etc).
    
    Args:
        date_str (str): Data.
        format (str, opcional): Formato da data.
        
    Returns:
        str: Descrição do período ou a data formatada se não for um período especial.
    """
    try:
        date_obj = datetime.datetime.strptime(date_str, format).date()
        today = datetime.date.today()
        
        if date_obj == today:
            return "Hoje"
        
        if date_obj == today - datetime.timedelta(days=1):
            return "Ontem"
        
        if date_obj == today + datetime.timedelta(days=1):
            return "Amanhã"
        
        # Verificar se está na mesma semana
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        
        if start_of_week <= date_obj <= end_of_week:
            return f"{get_date_weekday(date_str, format)}"
        
        # Verificar se é na próxima semana
        next_week_start = start_of_week + datetime.timedelta(days=7)
        next_week_end = end_of_week + datetime.timedelta(days=7)
        
        if next_week_start <= date_obj <= next_week_end:
            return f"Próx. {get_date_weekday(date_str, format)}"
        
        # Caso contrário, retornar a data formatada
        return format_date(date_str, format, "%d/%m/%Y")
        
    except Exception:
        return format_date(date_str, format, "%d/%m/%Y")