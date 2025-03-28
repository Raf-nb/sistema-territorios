#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QLineEdit, QComboBox, QSpinBox,
                              QDateEdit, QTimeEdit, QTextEdit, QFormLayout,
                              QDialogButtonBox, QCheckBox)
from PySide6.QtCore import Qt, QDate, QTime
from typing import Dict, Any, Optional, List, Tuple

class InputDialog(QDialog):
    """Diálogo para entrada de dados"""
    
    def __init__(self, parent=None, title="Entrada de Dados", 
                 fields=None, values=None, required_fields=None):
        """
        Inicializa o diálogo de entrada de dados
        
        Args:
            parent: Widget pai
            title: Título do diálogo
            fields: Lista de campos no formato (nome, tipo, label, [opções])
                nome: nome do campo (usado como chave no dicionário de valores)
                tipo: 'text', 'combo', 'date', 'time', 'number', 'textarea', 'checkbox'
                label: rótulo do campo
                opções: para 'combo', lista de tuplas (valor, texto)
            values: Dicionário com valores iniciais dos campos
            required_fields: Lista de nomes de campos obrigatórios
        """
        super().__init__(parent)
        
        self.fields = fields or []
        self.values = values or {}
        self.required_fields = required_fields or []
        self.widgets = {}  # Para armazenar referências aos widgets
        
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        self.setModal(True)
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface do diálogo"""
        layout = QVBoxLayout(self)
        
        # Formulário de campos
        form_layout = QFormLayout()
        
        for field in self.fields:
            field_name, field_type, field_label = field[:3]
            field_options = field[3] if len(field) > 3 else []
            
            # Criar o widget apropriado para o tipo de campo
            if field_type == 'text':
                widget = QLineEdit()
                if field_name in self.values:
                    widget.setText(str(self.values[field_name] or ""))
            
            elif field_type == 'combo':
                widget = QComboBox()
                for value, text in field_options:
                    widget.addItem(text, value)
                if field_name in self.values:
                    for i in range(widget.count()):
                        if widget.itemData(i) == self.values[field_name]:
                            widget.setCurrentIndex(i)
                            break
            
            elif field_type == 'date':
                widget = QDateEdit(QDate.currentDate())
                widget.setCalendarPopup(True)
                widget.setDisplayFormat("dd/MM/yyyy")
                if field_name in self.values and self.values[field_name]:
                    try:
                        date = QDate.fromString(self.values[field_name], "yyyy-MM-dd")
                        widget.setDate(date)
                    except:
                        pass
            
            elif field_type == 'time':
                widget = QTimeEdit(QTime.currentTime())
                widget.setDisplayFormat("HH:mm")
                if field_name in self.values and self.values[field_name]:
                    try:
                        time_parts = self.values[field_name].split(":")
                        time = QTime(int(time_parts[0]), int(time_parts[1]))
                        widget.setTime(time)
                    except:
                        pass
            
            elif field_type == 'number':
                widget = QSpinBox()
                widget.setRange(0, 999999)
                if field_name in self.values:
                    widget.setValue(int(self.values[field_name] or 0))
            
            elif field_type == 'textarea':
                widget = QTextEdit()
                if field_name in self.values:
                    widget.setText(str(self.values[field_name] or ""))
            
            elif field_type == 'checkbox':
                widget = QCheckBox()
                if field_name in self.values:
                    widget.setChecked(bool(self.values[field_name]))
            
            else:
                widget = QLineEdit()  # Padrão para tipos desconhecidos
                if field_name in self.values:
                    widget.setText(str(self.values[field_name] or ""))
            
            # Adicionar rótulo de campo obrigatório
            if field_name in self.required_fields:
                field_label = f"{field_label} *"
            
            # Adicionar o widget ao formulário
            form_layout.addRow(field_label, widget)
            
            # Armazenar a referência ao widget
            self.widgets[field_name] = widget
        
        layout.addLayout(form_layout)
        
        # Botões padrão OK/Cancelar
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        
        # Estilizar botão OK
        ok_button = buttons.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setText("Salvar")
        ok_button.setStyleSheet("background-color: #4CAF50; color: white;")
        
        layout.addWidget(buttons)
        
        # Nota sobre campos obrigatórios
        if self.required_fields:
            note_label = QLabel("* Campos obrigatórios")
            note_label.setStyleSheet("color: gray; font-size: 10px;")
            note_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(note_label)
    
    def validate_and_accept(self):
        """Valida os dados antes de aceitar o diálogo"""
        # Verificar campos obrigatórios
        for field_name in self.required_fields:
            if field_name not in self.widgets:
                continue
                
            widget = self.widgets[field_name]
            
            if isinstance(widget, QLineEdit) and not widget.text().strip():
                widget.setStyleSheet("border: 1px solid red;")
                return
            elif isinstance(widget, QTextEdit) and not widget.toPlainText().strip():
                widget.setStyleSheet("border: 1px solid red;")
                return
            elif isinstance(widget, QComboBox) and widget.currentData() is None:
                widget.setStyleSheet("border: 1px solid red;")
                return
        
        # Se chegou até aqui, todos os campos obrigatórios estão preenchidos
        self.accept()
    
    def get_values(self) -> Dict[str, Any]:
        """Retorna um dicionário com os valores dos campos"""
        values = {}
        
        for field_name, widget in self.widgets.items():
            # Obter o valor do widget de acordo com seu tipo
            if isinstance(widget, QLineEdit):
                values[field_name] = widget.text().strip() or None
            
            elif isinstance(widget, QComboBox):
                values[field_name] = widget.currentData()
            
            elif isinstance(widget, QDateEdit):
                values[field_name] = widget.date().toString("yyyy-MM-dd")
            
            elif isinstance(widget, QTimeEdit):
                values[field_name] = widget.time().toString("HH:mm")
            
            elif isinstance(widget, QSpinBox):
                values[field_name] = widget.value()
            
            elif isinstance(widget, QTextEdit):
                values[field_name] = widget.toPlainText().strip() or None
            
            elif isinstance(widget, QCheckBox):
                values[field_name] = widget.isChecked()
        
        return values
    
    @staticmethod
    def get_data(parent=None, title="Entrada de Dados", 
                fields=None, values=None, required_fields=None) -> Tuple[bool, Dict[str, Any]]:
        """
        Exibe um diálogo de entrada de dados e retorna os valores
        
        Args:
            parent: Widget pai
            title: Título do diálogo
            fields: Lista de campos no formato (nome, tipo, label, [opções])
            values: Dicionário com valores iniciais dos campos
            required_fields: Lista de nomes de campos obrigatórios
            
        Returns:
            Tuple[bool, Dict[str, Any]]: (sucesso, valores)
        """
        dialog = InputDialog(parent, title, fields, values, required_fields)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            return (True, dialog.get_values())
        else:
            return (False, {})