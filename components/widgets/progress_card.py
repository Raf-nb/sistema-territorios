#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QProgressBar, QFrame)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QFont

class ProgressCard(QWidget):
    """Widget de cartão com título, valor e barra de progresso"""
    
    def __init__(self, parent=None, title="", value=0, max_value=100, 
                 icon=None, show_percentage=True, color=None):
        """
        Inicializa o widget de cartão de progresso
        
        Args:
            parent: Widget pai
            title: Título do cartão
            value: Valor atual
            max_value: Valor máximo
            icon: Ícone opcional
            show_percentage: Se deve mostrar o percentual
            color: Cor opcional para a barra de progresso
        """
        super().__init__(parent)
        
        self.title = title
        self.value = value
        self.max_value = max_value
        self.icon = icon
        self.show_percentage = show_percentage
        self.color = color
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout(self)
        
        # Estilizar o widget como um cartão
        self.setStyleSheet("""
            ProgressCard {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
            }
        """)
        
        # Título com ícone (opcional)
        title_layout = QHBoxLayout()
        
        if self.icon:
            icon_label = QLabel()
            icon_label.setPixmap(self.icon.pixmap(QSize(24, 24)))
            title_layout.addWidget(icon_label)
        
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-weight: bold; color: #333;")
        title_layout.addWidget(self.title_label)
        
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #E0E0E0;")
        layout.addWidget(separator)
        
        # Valor e percentual
        value_layout = QHBoxLayout()
        
        # Valor principal
        percentage = int((self.value / self.max_value) * 100) if self.max_value > 0 else 0
        
        value_text = f"{self.value}/{self.max_value}"
        if self.show_percentage:
            value_text += f" ({percentage}%)"
            
        self.value_label = QLabel(value_text)
        self.value_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_layout.addWidget(self.value_label)
        
        layout.addLayout(value_layout)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self.max_value)
        self.progress_bar.setValue(self.value)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        
        # Aplicar cor personalizada se definida
        if self.color:
            self.progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: #F5F5F5;
                    border-radius: 4px;
                    border: none;
                }}
                QProgressBar::chunk {{
                    background-color: {self.color};
                    border-radius: 4px;
                }}
            """)
        
        layout.addWidget(self.progress_bar)
    
    def set_value(self, value):
        """Atualiza o valor do cartão"""
        self.value = value
        self.progress_bar.setValue(value)
        
        # Atualizar o texto do valor
        percentage = int((self.value / self.max_value) * 100) if self.max_value > 0 else 0
        
        value_text = f"{self.value}/{self.max_value}"
        if self.show_percentage:
            value_text += f" ({percentage}%)"
            
        self.value_label.setText(value_text)
    
    def set_max_value(self, max_value):
        """Atualiza o valor máximo do cartão"""
        self.max_value = max_value
        self.progress_bar.setMaximum(max_value)
        
        # Atualizar o texto do valor também
        self.set_value(self.value)
    
    def set_title(self, title):
        """Atualiza o título do cartão"""
        self.title = title
        self.title_label.setText(title)
    
    def set_color(self, color):
        """Atualiza a cor da barra de progresso"""
        self.color = color
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #F5F5F5;
                border-radius: 4px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {self.color};
                border-radius: 4px;
            }}
        """)