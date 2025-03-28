#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funções para gerenciamento de backup do banco de dados.
"""

import os
import shutil
import time
from datetime import datetime, timedelta
import sqlite3

from utils.config_reader import get_config, get_config_path

def create_backup(db_path=None, backup_dir=None):
    """
    Cria um backup do banco de dados.
    
    Args:
        db_path (str, opcional): Caminho para o arquivo de banco de dados.
            Se não fornecido, usa o caminho das configurações.
        backup_dir (str, opcional): Diretório onde o backup será salvo.
            Se não fornecido, usa o diretório das configurações.
    
    Returns:
        str: Caminho para o arquivo de backup criado, ou None em caso de erro.
    """
    config = get_config()
    
    # Usar valores padrão das configurações, se não fornecidos
    if not db_path:
        db_path = get_config_path(config['database']['path'])
    
    if not backup_dir:
        backup_dir = get_config_path(config['database']['backup_dir'])
    
    # Verificar se o arquivo de banco de dados existe
    if not os.path.exists(db_path):
        print(f"Arquivo de banco de dados não encontrado: {db_path}")
        return None
    
    # Certificar-se de que o diretório de backup existe
    os.makedirs(backup_dir, exist_ok=True)
    
    # Gerar nome para o arquivo de backup com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Verificar se o banco de dados está em uso
        conn = None
        try:
            # Tentar abrir o banco de dados para verificar se está disponível
            conn = sqlite3.connect(db_path)
            # Executar vacuum para otimizar o banco de dados antes do backup
            conn.execute("VACUUM")
            conn.close()
        except sqlite3.Error as e:
            print(f"Aviso: Não foi possível otimizar o banco de dados: {e}")
            if conn:
                conn.close()
        
        # Fazer uma cópia do arquivo
        shutil.copy2(db_path, backup_path)
        print(f"Backup criado com sucesso: {backup_path}")
        
        # Limpar backups antigos
        clean_old_backups(backup_dir)
        
        return backup_path
    except Exception as e:
        print(f"Erro ao criar backup: {e}")
        return None

def clean_old_backups(backup_dir=None, max_days=None, max_files=None):
    """
    Remove backups antigos para economizar espaço.
    
    Args:
        backup_dir (str, opcional): Diretório de backups.
        max_days (int, opcional): Número máximo de dias para manter os backups.
        max_files (int, opcional): Número máximo de arquivos de backup para manter.
    """
    config = get_config()
    
    if not backup_dir:
        backup_dir = get_config_path(config['database']['backup_dir'])
    
    if not max_days:
        max_days = config['database'].get('backup_retention_days', 30)
    
    if not max_files:
        max_files = config['database'].get('max_backup_files', 10)
    
    # Verificar se o diretório existe
    if not os.path.exists(backup_dir):
        return
    
    try:
        # Obter lista de arquivos de backup
        backups = []
        for filename in os.listdir(backup_dir):
            if filename.startswith("backup_") and filename.endswith(".db"):
                file_path = os.path.join(backup_dir, filename)
                file_time = os.path.getmtime(file_path)
                backups.append((file_path, file_time))
        
        # Remover backups por data
        if max_days > 0:
            cutoff_time = time.time() - (max_days * 86400)  # 86400 segundos = 1 dia
            for file_path, file_time in backups:
                if file_time < cutoff_time:
                    try:
                        os.remove(file_path)
                        print(f"Backup antigo removido: {file_path}")
                    except Exception as e:
                        print(f"Erro ao remover backup antigo {file_path}: {e}")
        
        # Remover backups por limite de arquivos
        if max_files > 0:
            # Ordenar por data (mais recente primeiro)
            backups.sort(key=lambda x: x[1], reverse=True)
            
            # Remover backups excedentes
            for file_path, _ in backups[max_files:]:
                try:
                    os.remove(file_path)
                    print(f"Backup excedente removido: {file_path}")
                except Exception as e:
                    print(f"Erro ao remover backup excedente {file_path}: {e}")
    
    except Exception as e:
        print(f"Erro ao limpar backups antigos: {e}")

def restore_backup(backup_path, db_path=None):
    """
    Restaura um backup para o banco de dados principal.
    
    Args:
        backup_path (str): Caminho para o arquivo de backup.
        db_path (str, opcional): Caminho para o banco de dados principal.
            Se não fornecido, usa o caminho das configurações.
    
    Returns:
        bool: True se o backup foi restaurado com sucesso, False caso contrário.
    """
    config = get_config()
    
    if not db_path:
        db_path = get_config_path(config['database']['path'])
    
    # Verificar se o arquivo de backup existe
    if not os.path.exists(backup_path):
        print(f"Arquivo de backup não encontrado: {backup_path}")
        return False
    
    try:
        # Fazer um backup do banco atual antes de restaurar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_backup = f"{db_path}.before_restore_{timestamp}"
        
        # Verificar se o banco de dados atual existe antes de fazer backup
        if os.path.exists(db_path):
            shutil.copy2(db_path, temp_backup)
            print(f"Backup temporário criado: {temp_backup}")
        
        # Restaurar o backup
        shutil.copy2(backup_path, db_path)
        print(f"Backup restaurado com sucesso: {backup_path}")
        return True
    
    except Exception as e:
        print(f"Erro ao restaurar backup: {e}")
        
        # Tentar recuperar do backup temporário se houver erro
        if os.path.exists(temp_backup):
            try:
                shutil.copy2(temp_backup, db_path)
                print(f"Banco de dados recuperado do backup temporário.")
            except Exception as recover_error:
                print(f"Erro na recuperação do banco de dados: {recover_error}")
        
        return False

def list_backups(backup_dir=None):
    """
    Lista todos os backups disponíveis.
    
    Args:
        backup_dir (str, opcional): Diretório de backups.
    
    Returns:
        list: Lista de dicionários com informações dos backups.
    """
    config = get_config()
    
    if not backup_dir:
        backup_dir = get_config_path(config['database']['backup_dir'])
    
    # Verificar se o diretório existe
    if not os.path.exists(backup_dir):
        return []
    
    backups = []
    
    try:
        for filename in os.listdir(backup_dir):
            if filename.startswith("backup_") and filename.endswith(".db"):
                file_path = os.path.join(backup_dir, filename)
                file_stats = os.stat(file_path)
                
                # Extrair timestamp do nome do arquivo
                try:
                    # Formato: backup_AAAAMMDD_HHMMSS.db
                    date_str = filename[7:15]  # AAAAMMDD
                    time_str = filename[16:22]  # HHMMSS
                    timestamp = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]} {time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
                except:
                    # Se não conseguir extrair do nome, usar a data de modificação
                    timestamp = datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                
                # Calcular tamanho legível
                size_bytes = file_stats.st_size
                size_readable = format_file_size(size_bytes)
                
                backups.append({
                    'path': file_path,
                    'filename': filename,
                    'timestamp': timestamp,
                    'size': size_bytes,
                    'size_readable': size_readable,
                    'mtime': file_stats.st_mtime
                })
        
        # Ordenar por data de modificação (mais recente primeiro)
        backups.sort(key=lambda x: x['mtime'], reverse=True)
        
        return backups
    
    except Exception as e:
        print(f"Erro ao listar backups: {e}")
        return []

def format_file_size(size_bytes):
    """
    Formata o tamanho do arquivo em uma string legível.
    
    Args:
        size_bytes (int): Tamanho em bytes.
    
    Returns:
        str: Tamanho formatado.
    """
    # Converter bytes para KB, MB ou GB conforme necessário
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"