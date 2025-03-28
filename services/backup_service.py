#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from datetime import datetime
from typing import List, Optional

class BackupService:
    """Serviço para gerenciar backups do banco de dados"""
    
    def __init__(self, db_path: str, backup_dir: str):
        self.db_path = db_path
        self.backup_dir = backup_dir
        
        # Criar o diretório de backup se não existir
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
    
    def criar_backup(self) -> Optional[str]:
        """Cria um backup do banco de dados atual"""
        try:
            # Verificar se o arquivo do banco de dados existe
            if not os.path.isfile(self.db_path):
                print(f"Erro: Arquivo de banco de dados não encontrado: {self.db_path}")
                return None
            
            # Criar nome do arquivo de backup com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Copiar o arquivo
            shutil.copy2(self.db_path, backup_path)
            print(f"Backup criado com sucesso: {backup_path}")
            
            # Limpar backups antigos (manter os últimos 10)
            self._limpar_backups_antigos(10)
            
            return backup_path
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return None
    
    def restaurar_backup(self, backup_path: str) -> bool:
        """Restaura um backup específico"""
        try:
            if not os.path.isfile(backup_path):
                print(f"Erro: Arquivo de backup não encontrado: {backup_path}")
                return False
            
            # Fazer backup do banco atual antes de restaurar (por segurança)
            self.criar_backup()
            
            # Restaurar o backup
            shutil.copy2(backup_path, self.db_path)
            print(f"Backup restaurado com sucesso: {backup_path}")
            return True
        except Exception as e:
            print(f"Erro ao restaurar backup: {e}")
            return False
    
    def listar_backups(self) -> List[dict]:
        """Lista todos os backups disponíveis"""
        backups = []
        
        try:
            # Verificar todos os arquivos no diretório de backup
            for filename in os.listdir(self.backup_dir):
                if filename.startswith("backup_") and filename.endswith(".db"):
                    file_path = os.path.join(self.backup_dir, filename)
                    
                    # Extrair timestamp do nome do arquivo (formato: backup_YYYYMMDD_HHMMSS.db)
                    try:
                        timestamp_str = filename[7:-3]  # Remove "backup_" e ".db"
                        created_at = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    except:
                        created_at = datetime.fromtimestamp(os.path.getctime(file_path))
                    
                    # Obter tamanho do arquivo
                    size_bytes = os.path.getsize(file_path)
                    size_mb = size_bytes / (1024 * 1024)
                    
                    backups.append({
                        'filename': filename,
                        'path': file_path,
                        'created_at': created_at,
                        'size_bytes': size_bytes,
                        'size_mb': round(size_mb, 2)
                    })
            
            # Ordenar por data de criação (mais recente primeiro)
            backups.sort(key=lambda x: x['created_at'], reverse=True)
            
        except Exception as e:
            print(f"Erro ao listar backups: {e}")
        
        return backups
    
    def _limpar_backups_antigos(self, manter_quantidade: int = 10):
        """Remove backups antigos, mantendo apenas a quantidade especificada"""
        backups = self.listar_backups()
        
        # Se tivermos mais backups que o limite, remover os mais antigos
        if len(backups) > manter_quantidade:
            for backup in backups[manter_quantidade:]:
                try:
                    os.remove(backup['path'])
                    print(f"Backup antigo removido: {backup['filename']}")
                except Exception as e:
                    print(f"Erro ao remover backup antigo {backup['filename']}: {e}")