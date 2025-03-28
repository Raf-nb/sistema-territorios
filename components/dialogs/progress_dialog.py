#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QProgressBar, QDialogButtonBox)
from PySide6.QtCore import Qt, Signal, Slot, QTimer

class ProgressDialog(QDialog):
    """Diálogo para exibir progresso de operações"""
    
    cancelRequested = Signal()  # Sinal emitido quando o usuário solicita cancelamento
    
    def __init__(self, parent=None, title="Operação em Andamento", 
                 message="Por favor, aguarde enquanto a operação é realizada...",
                 cancellable=True, auto_close=True, min_value=0, max_value=100):
        """
        Inicializa o diálogo de progresso
        
        Args:
            parent: Widget pai
            title: Título do diálogo
            message: Mensagem a ser exibida
            cancellable: Se o usuário pode cancelar a operação
            auto_close: Se o diálogo deve fechar automaticamente quando o progresso atingir 100%
            min_value: Valor mínimo do progresso
            max_value: Valor máximo do progresso
        """
        super().__init__(parent)
        
        self.auto_close = auto_close
        self.cancelled = False
        
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.setModal(True)
        
        # Impedir que o diálogo seja fechado pelo X
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        
        self.init_ui(message, cancellable, min_value, max_value)
    
    def init_ui(self, message, cancellable, min_value, max_value):
        """Inicializa a interface do diálogo"""
        layout = QVBoxLayout(self)
        
        # Mensagem
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(min_value, max_value)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: gray;")
        layout.addWidget(self.status_label)
        
        # Botões
        buttons = QDialogButtonBox()
        
        if cancellable:
            cancel_button = QPushButton("Cancelar")
            cancel_button.clicked.connect(self.request_cancel)
            buttons.addButton(cancel_button, QDialogButtonBox.ButtonRole.RejectRole)
        
        layout.addWidget(buttons)
    
    def set_progress(self, value, status=None):
        """
        Atualiza o valor da barra de progresso
        
        Args:
            value: Novo valor do progresso
            status: Texto de status opcional
        """
        self.progress_bar.setValue(value)
        
        if status:
            self.status_label.setText(status)
        
        # Fechar automaticamente quando atingir o máximo
        if self.auto_close and value >= self.progress_bar.maximum():
            # Pequeno atraso para o usuário ver o progresso completo
            QTimer.singleShot(500, self.accept)
    
    def set_range(self, minimum, maximum):
        """Define o intervalo da barra de progresso"""
        self.progress_bar.setRange(minimum, maximum)
    
    def set_message(self, message):
        """Atualiza a mensagem do diálogo"""
        self.message_label.setText(message)
    
    def is_cancelled(self) -> bool:
        """Retorna se o usuário solicitou cancelamento"""
        return self.cancelled
    
    @Slot()
    def request_cancel(self):
        """Solicita o cancelamento da operação"""
        self.cancelled = True
        self.cancelRequested.emit()
        self.status_label.setText("Cancelando operação...")
        self.status_label.setStyleSheet("color: #f44336;")