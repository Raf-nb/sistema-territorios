#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

class ConfirmationDialog(QDialog):
    """Diálogo de confirmação para ações importantes"""
    
    def __init__(self, parent=None, title="Confirmar Ação", 
                 message="Tem certeza que deseja realizar esta ação?",
                 confirm_text="Confirmar", cancel_text="Cancelar",
                 icon=QMessageBox.Icon.Question):
        super().__init__(parent)
        
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.setModal(True)
        
        self.init_ui(message, confirm_text, cancel_text, icon)
    
    def init_ui(self, message, confirm_text, cancel_text, icon):
        """Inicializa a interface do diálogo"""
        layout = QVBoxLayout(self)
        
        # Área da mensagem
        message_layout = QHBoxLayout()
        
        # Ícone
        icon_label = QLabel()
        if icon == QMessageBox.Icon.Question:
            icon_label.setPixmap(QIcon.fromTheme("dialog-question").pixmap(32, 32))
        elif icon == QMessageBox.Icon.Warning:
            icon_label.setPixmap(QIcon.fromTheme("dialog-warning").pixmap(32, 32))
        elif icon == QMessageBox.Icon.Critical:
            icon_label.setPixmap(QIcon.fromTheme("dialog-error").pixmap(32, 32))
        elif icon == QMessageBox.Icon.Information:
            icon_label.setPixmap(QIcon.fromTheme("dialog-information").pixmap(32, 32))
        message_layout.addWidget(icon_label)
        
        # Mensagem
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        message_layout.addWidget(message_label, 1)
        
        layout.addLayout(message_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_button = QPushButton(cancel_text)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)
        
        confirm_button = QPushButton(confirm_text)
        confirm_button.setDefault(True)
        if icon == QMessageBox.Icon.Warning or icon == QMessageBox.Icon.Critical:
            confirm_button.setStyleSheet("background-color: #f44336; color: white;")
        else:
            confirm_button.setStyleSheet("background-color: #4CAF50; color: white;")
        confirm_button.clicked.connect(self.accept)
        buttons_layout.addWidget(confirm_button)
        
        layout.addLayout(buttons_layout)
    
    @staticmethod
    def confirm(parent=None, title="Confirmar Ação", 
                message="Tem certeza que deseja realizar esta ação?",
                confirm_text="Confirmar", cancel_text="Cancelar",
                icon=QMessageBox.Icon.Question) -> bool:
        """
        Exibe um diálogo de confirmação e retorna True se o usuário confirmar
        
        Args:
            parent: Widget pai para o diálogo
            title: Título da janela
            message: Mensagem a ser exibida
            confirm_text: Texto do botão de confirmação
            cancel_text: Texto do botão de cancelamento
            icon: Ícone a ser exibido (QMessageBox.Icon)
            
        Returns:
            bool: True se o usuário confirmar, False caso contrário
        """
        dialog = ConfirmationDialog(
            parent, title, message, confirm_text, cancel_text, icon
        )
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted
    
    @staticmethod
    def confirm_delete(parent=None, item_name="item") -> bool:
        """
        Exibe um diálogo de confirmação de exclusão
        
        Args:
            parent: Widget pai para o diálogo
            item_name: Nome do item a ser excluído
            
        Returns:
            bool: True se o usuário confirmar, False caso contrário
        """
        return ConfirmationDialog.confirm(
            parent,
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o {item_name}?\nEsta ação não pode ser desfeita.",
            "Excluir",
            "Cancelar",
            QMessageBox.Icon.Warning
        )