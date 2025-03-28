#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime
from typing import List, Optional

class LogSistema:
    """Classe para gerenciar logs do sistema em arquivo"""
    
    # Níveis de log
    NIVEL_DEBUG = logging.DEBUG
    NIVEL_INFO = logging.INFO
    NIVEL_AVISO = logging.WARNING
    NIVEL_ERRO = logging.ERROR
    NIVEL_CRITICO = logging.CRITICAL
    
    def __init__(self, log_dir: str = "logs", log_level: int = logging.INFO):
        self.log_dir = log_dir
        self.log_level = log_level
        self.logger = None
        
        # Criar diretório de logs se não existir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self._configurar_logger()
    
    def _configurar_logger(self):
        """Configura o logger do sistema"""
        # Nome do arquivo com a data atual
        hoje = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.log_dir, f"sistema_{hoje}.log")
        
        # Configurar o logger
        self.logger = logging.getLogger("sistema")
        self.logger.setLevel(self.log_level)
        
        # Remover handlers existentes para evitar duplicados
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Criar um file handler para escrever no arquivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        
        # Criar um formato de log
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # Adicionar o handler ao logger
        self.logger.addHandler(file_handler)
    
    def debug(self, mensagem: str):
        """Registra uma mensagem de debug"""
        self.logger.debug(mensagem)
    
    def info(self, mensagem: str):
        """Registra uma mensagem informativa"""
        self.logger.info(mensagem)
    
    def aviso(self, mensagem: str):
        """Registra um aviso"""
        self.logger.warning(mensagem)
    
    def erro(self, mensagem: str):
        """Registra um erro"""
        self.logger.error(mensagem)
    
    def critico(self, mensagem: str):
        """Registra um erro crítico"""
        self.logger.critical(mensagem)
    
    def registrar(self, nivel: int, mensagem: str):
        """Registra uma mensagem com o nível especificado"""
        self.logger.log(nivel, mensagem)
    
    def ler_logs(self, data: str = None, nivel: int = None, limit: int = 100) -> List[str]:
        """Lê os logs do arquivo"""
        try:
            # Se não for informada uma data, usa a data atual
            if data is None:
                data = datetime.now().strftime("%Y-%m-%d")
            
            log_file = os.path.join(self.log_dir, f"sistema_{data}.log")
            
            # Verificar se o arquivo existe
            if not os.path.exists(log_file):
                return []
            
            # Ler as linhas do arquivo
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Filtrar por nível se necessário
            if nivel is not None:
                nivel_str = logging.getLevelName(nivel)
                lines = [line for line in lines if f"[{nivel_str}]" in line]
            
            # Retornar as últimas linhas
            return lines[-limit:]
        except Exception as e:
            print(f"Erro ao ler logs: {e}")
            return []