#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arquivo principal que inicializa o Sistema de Controle de Territórios.
"""

import sys
import os

def setup_environment():
    """
    Configura o ambiente da aplicação.
    Adiciona os diretórios necessários ao sys.path.
    """
    # Adiciona o diretório atual (raiz do projeto) ao path
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    
    # Configura variáveis de ambiente, se necessário
    os.environ['APP_ROOT'] = root_dir

def run_app():
    """
    Inicializa e executa a aplicação.
    """
    setup_environment()
    
    # Importa após configurar o ambiente
    from core.app import main
    
    # Executa a aplicação
    main()

if __name__ == "__main__":
    run_app()