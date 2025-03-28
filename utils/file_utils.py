#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários para operações com arquivos.
"""

import os
import shutil
import tempfile
import json
import csv
from typing import List, Dict, Any, Optional, Union, TextIO, BinaryIO
from datetime import datetime
import platform
import subprocess

def ensure_directory(directory_path: str) -> bool:
    """
    Garante que um diretório existe, criando-o se necessário.
    
    Args:
        directory_path (str): Caminho do diretório.
        
    Returns:
        bool: True se o diretório existe ou foi criado com sucesso, False caso contrário.
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Erro ao criar diretório {directory_path}: {e}")
        return False

def get_file_extension(file_path: str) -> str:
    """
    Obtém a extensão de um arquivo.
    
    Args:
        file_path (str): Caminho do arquivo.
        
    Returns:
        str: Extensão do arquivo (sem o ponto).
    """
    return os.path.splitext(file_path)[1][1:].lower()

def get_file_size(file_path: str) -> int:
    """
    Obtém o tamanho de um arquivo em bytes.
    
    Args:
        file_path (str): Caminho do arquivo.
        
    Returns:
        int: Tamanho do arquivo em bytes.
    """
    try:
        return os.path.getsize(file_path)
    except Exception:
        return 0

def format_file_size(size_bytes: int) -> str:
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

def read_text_file(file_path: str, encoding: str = "utf-8") -> Optional[str]:
    """
    Lê o conteúdo de um arquivo de texto.
    
    Args:
        file_path (str): Caminho do arquivo.
        encoding (str, opcional): Codificação do arquivo.
        
    Returns:
        Optional[str]: Conteúdo do arquivo ou None em caso de erro.
    """
    try:
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}")
        return None

def write_text_file(file_path: str, content: str, encoding: str = "utf-8") -> bool:
    """
    Escreve conteúdo em um arquivo de texto.
    
    Args:
        file_path (str): Caminho do arquivo.
        content (str): Conteúdo a ser escrito.
        encoding (str, opcional): Codificação do arquivo.
        
    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário.
    """
    try:
        # Garantir que o diretório do arquivo existe
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # Escrever o arquivo com segurança (primeiro em um arquivo temporário)
        temp_file = tempfile.NamedTemporaryFile(mode="w", encoding=encoding, delete=False)
        try:
            with temp_file:
                temp_file.write(content)
            
            # Em sistemas Windows, é preciso fechar o arquivo antes de movê-lo
            shutil.move(temp_file.name, file_path)
            return True
        finally:
            # Garantir que o arquivo temporário seja removido em caso de erro
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    except Exception as e:
        print(f"Erro ao escrever arquivo {file_path}: {e}")
        return False

def read_json_file(file_path: str, encoding: str = "utf-8") -> Optional[Union[Dict, List]]:
    """
    Lê o conteúdo de um arquivo JSON.
    
    Args:
        file_path (str): Caminho do arquivo.
        encoding (str, opcional): Codificação do arquivo.
        
    Returns:
        Optional[Union[Dict, List]]: Conteúdo do arquivo como objeto Python ou None em caso de erro.
    """
    try:
        with open(file_path, "r", encoding=encoding) as file:
            return json.load(file)
    except Exception as e:
        print(f"Erro ao ler arquivo JSON {file_path}: {e}")
        return None

def write_json_file(file_path: str, content: Union[Dict, List], 
                   encoding: str = "utf-8", indent: int = 4) -> bool:
    """
    Escreve conteúdo em um arquivo JSON.
    
    Args:
        file_path (str): Caminho do arquivo.
        content (Union[Dict, List]): Conteúdo a ser escrito.
        encoding (str, opcional): Codificação do arquivo.
        indent (int, opcional): Recuo para formatação.
        
    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário.
    """
    try:
        # Garantir que o diretório do arquivo existe
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # Escrever o arquivo com segurança (primeiro em um arquivo temporário)
        temp_file = tempfile.NamedTemporaryFile(mode="w", encoding=encoding, delete=False)
        try:
            with temp_file:
                json.dump(content, temp_file, indent=indent, ensure_ascii=False)
            
            # Em sistemas Windows, é preciso fechar o arquivo antes de movê-lo
            shutil.move(temp_file.name, file_path)
            return True
        finally:
            # Garantir que o arquivo temporário seja removido em caso de erro
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    except Exception as e:
        print(f"Erro ao escrever arquivo JSON {file_path}: {e}")
        return False

def read_csv_file(file_path: str, delimiter: str = ",", has_header: bool = True, 
                 encoding: str = "utf-8") -> Optional[List[Dict[str, str]]]:
    """
    Lê o conteúdo de um arquivo CSV.
    
    Args:
        file_path (str): Caminho do arquivo.
        delimiter (str, opcional): Delimitador de campo.
        has_header (bool, opcional): Se o arquivo tem cabeçalho.
        encoding (str, opcional): Codificação do arquivo.
        
    Returns:
        Optional[List[Dict[str, str]]]: Lista de dicionários (cada linha como um dicionário) ou None em caso de erro.
    """
    try:
        with open(file_path, "r", newline="", encoding=encoding) as file:
            if has_header:
                reader = csv.DictReader(file, delimiter=delimiter)
                return list(reader)
            else:
                reader = csv.reader(file, delimiter=delimiter)
                data = list(reader)
                # Converter para lista de dicionários com índices como chaves
                return [dict(enumerate(row)) for row in data]
    except Exception as e:
        print(f"Erro ao ler arquivo CSV {file_path}: {e}")
        return None

def write_csv_file(file_path: str, data: List[Dict[str, Any]], 
                  fieldnames: Optional[List[str]] = None, delimiter: str = ",", 
                  encoding: str = "utf-8") -> bool:
    """
    Escreve dados em um arquivo CSV.
    
    Args:
        file_path (str): Caminho do arquivo.
        data (List[Dict[str, Any]]): Dados a serem escritos.
        fieldnames (List[str], opcional): Lista de nomes de campos.
        delimiter (str, opcional): Delimitador de campo.
        encoding (str, opcional): Codificação do arquivo.
        
    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário.
    """
    try:
        # Garantir que o diretório do arquivo existe
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # Se fieldnames não for especificado, usar as chaves do primeiro item
        if not fieldnames and data:
            fieldnames = list(data[0].keys())
        
        # Escrever o arquivo com segurança (primeiro em um arquivo temporário)
        temp_file = tempfile.NamedTemporaryFile(mode="w", encoding=encoding, newline="", delete=False)
        try:
            with temp_file:
                writer = csv.DictWriter(temp_file, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            
            # Em sistemas Windows, é preciso fechar o arquivo antes de movê-lo
            shutil.move(temp_file.name, file_path)
            return True
        finally:
            # Garantir que o arquivo temporário seja removido em caso de erro
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    except Exception as e:
        print(f"Erro ao escrever arquivo CSV {file_path}: {e}")
        return False

def list_files(directory_path: str, extension: Optional[str] = None, recursive: bool = False) -> List[str]:
    """
    Lista os arquivos em um diretório.
    
    Args:
        directory_path (str): Caminho do diretório.
        extension (str, opcional): Filtrar por extensão.
        recursive (bool, opcional): Buscar recursivamente nos subdiretórios.
        
    Returns:
        List[str]: Lista de caminhos de arquivos.
    """
    files = []
    
    try:
        if recursive:
            for root, _, filenames in os.walk(directory_path):
                for filename in filenames:
                    if extension and not filename.lower().endswith(f".{extension.lower()}"):
                        continue
                    files.append(os.path.join(root, filename))
        else:
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    if extension and not filename.lower().endswith(f".{extension.lower()}"):
                        continue
                    files.append(file_path)
    except Exception as e:
        print(f"Erro ao listar arquivos em {directory_path}: {e}")
    
    return files

def backup_file(file_path: str, backup_dir: Optional[str] = None) -> Optional[str]:
    """
    Cria um backup de um arquivo.
    
    Args:
        file_path (str): Caminho do arquivo a ser copiado.
        backup_dir (str, opcional): Diretório de backup. Se None, usa o mesmo diretório.
        
    Returns:
        Optional[str]: Caminho do arquivo de backup ou None em caso de erro.
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        # Determinar diretório de backup
        if backup_dir:
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, os.path.basename(file_path))
        else:
            backup_path = file_path
        
        # Adicionar timestamp ao nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(backup_path)
        backup_path = f"{name}_backup_{timestamp}{ext}"
        
        # Copiar o arquivo
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"Erro ao fazer backup do arquivo {file_path}: {e}")
        return None

def is_file_older_than(file_path: str, days: int) -> bool:
    """
    Verifica se um arquivo é mais antigo que um determinado número de dias.
    
    Args:
        file_path (str): Caminho do arquivo.
        days (int): Número de dias.
        
    Returns:
        bool: True se o arquivo for mais antigo que o número de dias especificado.
    """
    try:
        if not os.path.exists(file_path):
            return False
        
        file_time = os.path.getmtime(file_path)
        file_age_in_days = (datetime.now().timestamp() - file_time) / (60 * 60 * 24)
        
        return file_age_in_days > days
    except Exception as e:
        print(f"Erro ao verificar idade do arquivo {file_path}: {e}")
        return False

def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Obtém informações sobre um arquivo.
    
    Args:
        file_path (str): Caminho do arquivo.
        
    Returns:
        Dict[str, Any]: Dicionário com informações do arquivo.
    """
    result = {}
    
    try:
        if not os.path.exists(file_path):
            return {"exists": False}
        
        stat_info = os.stat(file_path)
        
        result = {
            "exists": True,
            "path": file_path,
            "name": os.path.basename(file_path),
            "extension": get_file_extension(file_path),
            "size": stat_info.st_size,
            "size_formatted": format_file_size(stat_info.st_size),
            "created": datetime.fromtimestamp(stat_info.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.fromtimestamp(stat_info.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "accessed": datetime.fromtimestamp(stat_info.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
            "is_dir": os.path.isdir(file_path),
            "is_file": os.path.isfile(file_path),
            "is_symlink": os.path.islink(file_path),
            "permissions": {
                "readable": os.access(file_path, os.R_OK),
                "writable": os.access(file_path, os.W_OK),
                "executable": os.access(file_path, os.X_OK)
            }
        }
    except Exception as e:
        print(f"Erro ao obter informações do arquivo {file_path}: {e}")
        result = {"exists": False, "error": str(e)}
    
    return result

def open_file_with_default_app(file_path: str) -> bool:
    """
    Abre um arquivo com o aplicativo padrão do sistema.
    
    Args:
        file_path (str): Caminho do arquivo.
        
    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário.
    """
    try:
        if not os.path.exists(file_path):
            return False
        
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", file_path])
        else:  # Linux/Unix
            subprocess.call(["xdg-open", file_path])
        
        return True
    except Exception as e:
        print(f"Erro ao abrir arquivo {file_path}: {e}")
        return False

def remove_old_files(directory_path: str, days: int, extension: Optional[str] = None) -> int:
    """
    Remove arquivos mais antigos que um determinado número de dias.
    
    Args:
        directory_path (str): Caminho do diretório.
        days (int): Número de dias.
        extension (str, opcional): Remover apenas arquivos com esta extensão.
        
    Returns:
        int: Número de arquivos removidos.
    """
    removed_count = 0
    
    try:
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            return 0
        
        files = list_files(directory_path, extension)
        
        for file_path in files:
            if is_file_older_than(file_path, days):
                try:
                    os.remove(file_path)
                    removed_count += 1
                except Exception as e:
                    print(f"Erro ao remover arquivo {file_path}: {e}")
    except Exception as e:
        print(f"Erro ao remover arquivos antigos em {directory_path}: {e}")
    
    return removed_count