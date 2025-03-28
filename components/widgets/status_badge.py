#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPalette, QBrush, QFont
from typing import Dict, Optional

class StatusBadge(QLabel):
    """Widget para exibir status em forma de badge/etiqueta"""
    
    # Cores padrão para status comuns
    DEFAULT_COLORS = {
        "ativo": "#4CAF50",       # Verde
        "inativo": "#9E9E9E",     # Cinza
        "pendente": "#FF9800",    # Laranja
        "concluido": "#2196F3",   # Azul
        "erro": "#F44336",        # Vermelho
        "aviso": "#FFC107",       # Amarelo
        "info": "#2196F3",        # Azul
        "sucesso": "#4CAF50",     # Verde
    }
    
    def __init__(self, text="", status=None, custom_color=None, parent=None):
        """
        Inicializa o widget de badge de status
        
        Args:
            text: Texto a ser exibido
            status: Status predefinido (usa cores padrão)
            custom_color: Cor personalizada (sobrepõe status)
            parent: Widget pai
        """
        super().__init__(text, parent)
        
        self.status = status
        self.custom_color = custom_color
        
        self.setup_style()
    
    def setup_style(self):
        """Configura o estilo do badge"""
        # Definir a cor de fundo
        color = self.get_color()
        
        # Calcular a cor do texto (preto ou branco) com base no contraste
        text_color = self.get_contrasting_text_color(color)
        
        # Configurar o estilo
        self.setStyleSheet(f"""
            padding: 3px 8px;
            border-radius: 10px;
            background-color: {color};
            color: {text_color};
            font-weight: bold;
            min-width: 60px;
            text-align: center;
        """)
        
        # Alinhar o texto ao centro
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def get_color(self) -> str:
        """Obtém a cor do badge com base no status ou cor personalizada"""
        if self.custom_color:
            return self.custom_color
        
        if self.status and self.status.lower() in self.DEFAULT_COLORS:
            return self.DEFAULT_COLORS[self.status.lower()]
        
        # Cor padrão se não encontrar
        return "#9E9E9E"  # Cinza
    
    def get_contrasting_text_color(self, background_color: str) -> str:
        """
        Determina se deve usar texto preto ou branco com base na cor de fundo
        
        Args:
            background_color: Cor de fundo em formato hex (#RRGGBB)
            
        Returns:
            str: "#000000" para preto ou "#FFFFFF" para branco
        """
        # Converter cor hex para RGB
        try:
            if background_color.startswith('#'):
                bg_color = background_color[1:]
            else:
                bg_color = background_color
            
            r = int(bg_color[0:2], 16)
            g = int(bg_color[2:4], 16)
            b = int(bg_color[4:6], 16)
            
            # Fórmula para calcular luminosidade (W3C recomendação)
            # Se a luminosidade for alta, usar texto preto, caso contrário branco
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            
            if luminance > 0.5:
                return "#000000"  # Preto
            else:
                return "#FFFFFF"  # Branco
                
        except Exception:
            # Em caso de erro, retornar branco
            return "#FFFFFF"
    
    def set_status(self, status: str):
        """Define o status do badge"""
        self.status = status
        self.custom_color = None
        self.setup_style()
        
        # Atualizar o texto se estiver vazio
        if not self.text():
            self.setText(status.capitalize())
    
    def set_color(self, color: str):
        """Define uma cor personalizada para o badge"""
        self.custom_color = color
        self.setup_style()
    
    def set_text_and_status(self, text: str, status: str):
        """Define tanto o texto quanto o status do badge"""
        self.setText(text)
        self.set_status(status)