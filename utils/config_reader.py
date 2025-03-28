#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitário para leitura e gerenciamento de configurações.
"""

import os
import json
import sys

def get_config():
    """
    Obtém as configurações da aplicação.
    
    Returns:
        dict: Dicionário com as configurações.
    """
    # Importa as configurações do módulo principal
    try:
        # Adiciona o diretório raiz ao path para importação correta
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)
            
        from config import CONFIG
        return CONFIG
    except ImportError:
        # Se falhar, retorna configurações padrão
        return get_default_config()

def get_default_config():
    """
    Retorna as configurações padrão caso o módulo de configuração não esteja disponível.
    
    Returns:
        dict: Configurações padrão.
    """
    return {
        "database": {
            "path": "database/territorios.db",
            "backup_dir": "backups/",
            "backup_interval_days": 7,
            "auto_backup": True
        },
        "ui": {
            "theme": "default",
            "language": "pt_BR",
            "font_size": "normal",
            "show_welcome": True
        }
    }

def save_config(config):
    """
    Salva as configurações em um arquivo JSON.
    
    Args:
        config (dict): Configurações a serem salvas.
    
    Returns:
        bool: True se as configurações foram salvas com sucesso, False caso contrário.
    """
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(root_dir, 'config.json')
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
        return False

def get_config_path(relative_path):
    """
    Obtém o caminho completo para um item de configuração de caminho.
    
    Args:
        relative_path (str): Caminho relativo configurado.
    
    Returns:
        str: Caminho absoluto baseado no diretório raiz da aplicação.
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root_dir, relative_path)

def ensure_dirs(config):
    """
    Garante que os diretórios necessários existam.
    
    Args:
        config (dict): Configurações contendo os caminhos de diretórios.
    """
    dirs_to_check = [
        config['database']['backup_dir'],
        config['paths']['icons'],
        config['paths']['styles'],
        config['paths']['templates'],
        config['paths']['exports'],
        os.path.dirname(config['debug']['log_file'])
    ]
    
    for directory in dirs_to_check:
        full_path = get_config_path(directory)
        if not os.path.exists(full_path):
            try:
                os.makedirs(full_path, exist_ok=True)
            except Exception as e:
                print(f"Erro ao criar diretório {full_path}: {e}")