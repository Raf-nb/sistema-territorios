#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arquivo de configuração global da aplicação.
Contém configurações padrão e carrega personalização de config.json, se existir.
"""

import os
import json

# Configurações padrão
DEFAULT_CONFIG = {
    # Configurações do banco de dados
    "database": {
        "path": "database/territorios.db",
        "backup_dir": "backups/",
        "backup_interval_days": 7,
        "auto_backup": True
    },
    
    # Configurações da interface do usuário
    "ui": {
        "theme": "default",
        "language": "pt_BR",
        "font_size": "normal",
        "show_welcome": True
    },
    
    # Configurações de sessão
    "session": {
        "timeout_minutes": 30,
        "remember_login": False
    },
    
    # Configurações de notificação
    "notifications": {
        "enabled": True,
        "check_interval_minutes": 15,
        "show_designacao_alerts": True,
        "alert_days_before": 5
    },
    
    # Configurações de relatório
    "reports": {
        "default_export_format": "pdf",
        "logo_path": "resources/logo.png",
        "max_cached_reports": 10
    },
    
    # Diretórios de recursos
    "paths": {
        "icons": "resources/icons/",
        "styles": "resources/styles/",
        "templates": "resources/templates/",
        "exports": "exports/"
    },
    
    # Modo de depuração
    "debug": {
        "enabled": False,
        "log_level": "INFO",
        "log_to_file": True,
        "log_file": "logs/app.log"
    }
}

# Versão da aplicação
APP_VERSION = "1.0.0"

# Carregar configurações personalizadas, se existirem
def load_config():
    """Carrega configurações personalizadas de um arquivo JSON, se disponível."""
    config = DEFAULT_CONFIG.copy()
    
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                
            # Mesclar configurações personalizadas com as padrões
            for section, settings in user_config.items():
                if section in config:
                    if isinstance(settings, dict):
                        config[section].update(settings)
                    else:
                        config[section] = settings
                else:
                    config[section] = settings
                
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
    
    return config

# Carregar configurações na inicialização
CONFIG = load_config()