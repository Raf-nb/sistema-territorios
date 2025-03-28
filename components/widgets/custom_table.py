#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView, 
                              QAbstractItemView, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLineEdit, QLabel, QComboBox, QMenu,
                              QAction, QApplication, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, Signal, Slot, QSortFilterProxyModel
from PySide6.QtGui import QIcon, QColor, QBrush, QFont
from typing import List, Dict, Any, Optional, Callable, Union, Tuple

class CustomTableWidget(QWidget):
    """Widget de tabela customizado com recursos avançados"""
    
    # Sinais
    itemSelected = Signal(dict)  # Emitido quando um item é selecionado
    doubleClicked = Signal(dict)  # Emitido quando um item é clicado duas vezes
    
    def __init__(self, parent=None, columns=None, data=None, 
                 sortable=True, filterable=True, show_export=True,
                 id_column=None, stretch_column=None):
        """
        Inicializa o widget de tabela customizado
        
        Args:
            parent: Widget pai
            columns: Lista de colunas no formato [(nome, título), ...]
            data: Lista de dicionários com dados
            sortable: Se a tabela pode ser ordenada
            filterable: Se a tabela pode ser filtrada
            show_export: Se deve mostrar botão de exportação
            id_column: Nome da coluna que contém o ID (opcional)
            stretch_column: Índice da coluna que deve se expandir (opcional)
        """
        super().__init__(parent)
        
        self.columns = columns or []
        self.data = data or []
        self.sortable = sortable
        self.filterable = filterable
        self.show_export = show_export
        self.id_column = id_column
        self.stretch_column = stretch_column
        
        # Formatadores de células personalizados
        self.cell_formatters = {}
        
        self.init_ui()
        
        # Preencher a tabela se tiver dados
        if data:
            self.set_data(data)
    
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Barra de ferramentas
        if self.filterable or self.show_export:
            toolbar_layout = QHBoxLayout()
            
            # Filtro
            if self.filterable:
                filter_label = QLabel("Filtrar:")
                toolbar_layout.addWidget(filter_label)
                
                self.filter_field = QComboBox()
                self.filter_field.addItem("Todos os campos", None)
                for i, (name, title) in enumerate(self.columns):
                    self.filter_field.addItem(title, name)
                toolbar_layout.addWidget(self.filter_field)
                
                self.filter_input = QLineEdit()
                self.filter_input.setPlaceholderText("Digite para filtrar...")
                self.filter_input.textChanged.connect(self.apply_filter)
                toolbar_layout.addWidget(self.filter_input, 1)
            
            # Espaçador
            toolbar_layout.addStretch()
            
            # Botão de exportação
            if self.show_export:
                export_button = QPushButton("Exportar")
                export_button.setIcon(QIcon.fromTheme("document-save"))
                export_button.clicked.connect(self.export_data)
                toolbar_layout.addWidget(export_button)
            
            layout.addLayout(toolbar_layout)
        
        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([title for _, title in self.columns])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.doubleClicked.connect(self.on_double_click)
        
        # Configurar coluna que deve se expandir
        if self.stretch_column is not None and 0 <= self.stretch_column < len(self.columns):
            self.table.horizontalHeader().setSectionResizeMode(
                self.stretch_column, QHeaderView.ResizeMode.Stretch
            )
        
        # Permitir ordenação
        self.table.setSortingEnabled(self.sortable)
        
        layout.addWidget(self.table)
    
    def set_data(self, data: List[Dict[str, Any]]):
        """Define os dados da tabela"""
        self.data = data
        self.reload_table()
    
    def reload_table(self):
        """Recarrega os dados na tabela"""
        self.table.setRowCount(0)
        
        # Aplicar filtro se houver
        filtered_data = self.apply_filter()
        
        # Preencher a tabela
        for row, item in enumerate(filtered_data):
            self.table.insertRow(row)
            
            for col, (column_name, _) in enumerate(self.columns):
                value = item.get(column_name, "")
                table_item = QTableWidgetItem(str(value if value is not None else ""))
                
                # Armazenar dados originais
                table_item.setData(Qt.ItemDataRole.UserRole, item)
                
                # Aplicar formatador personalizado, se existir
                if column_name in self.cell_formatters:
                    self.cell_formatters[column_name](table_item, item, column_name)
                
                self.table.setItem(row, col, table_item)
    
    def get_selected_data(self) -> Optional[Dict[str, Any]]:
        """Retorna os dados do item selecionado"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            return None
        
        # Obter o primeiro item da linha selecionada
        return selected_items[0].data(Qt.ItemDataRole.UserRole)
    
    def set_cell_formatter(self, column_name: str, formatter: Callable[[QTableWidgetItem, Dict[str, Any], str], None]):
        """
        Define um formatador personalizado para uma coluna
        
        Args:
            column_name: Nome da coluna
            formatter: Função formatadora que recebe (QTableWidgetItem, dados_completos, nome_coluna)
        """
        self.cell_formatters[column_name] = formatter
        # Recarregar a tabela para aplicar o formatador
        if self.data:
            self.reload_table()
    
    @Slot()
    def apply_filter(self) -> List[Dict[str, Any]]:
        """
        Aplica o filtro atual aos dados e retorna os dados filtrados
        
        Returns:
            List[Dict[str, Any]]: Dados filtrados
        """
        filtered_data = self.data
        
        if self.filterable and hasattr(self, 'filter_input') and self.filter_input.text():
            filter_text = self.filter_input.text().lower()
            
            # Verificar se é para filtrar em uma coluna específica
            filter_column = self.filter_field.currentData()
            
            # Filtrar os dados
            if filter_column:
                # Filtrar apenas na coluna especificada
                filtered_data = [
                    item for item in self.data
                    if filter_text in str(item.get(filter_column, "")).lower()
                ]
            else:
                # Filtrar em todas as colunas
                filtered_data = []
                for item in self.data:
                    # Verificar se o texto de filtro está em algum campo
                    for column_name, _ in self.columns:
                        if filter_text in str(item.get(column_name, "")).lower():
                            filtered_data.append(item)
                            break
        
        # Se estiver recarregando a tabela, atualizar os dados
        if self.sender() == self.filter_input:
            self.reload_table()
        
        return filtered_data
    
    @Slot()
    def export_data(self):
        """Exporta os dados da tabela para CSV"""
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Exportar Dados", "", "Arquivos CSV (*.csv)"
        )
        
        if not filepath:
            return
        
        # Adicionar extensão .csv se não tiver
        if not filepath.endswith('.csv'):
            filepath += '.csv'
        
        try:
            import csv
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escrever cabeçalho
                writer.writerow([title for _, title in self.columns])
                
                # Escrever dados
                for item in self.apply_filter():
                    row_data = [str(item.get(name, "")) for name, _ in self.columns]
                    writer.writerow(row_data)
            
            QMessageBox.information(
                self, "Exportação Concluída", 
                f"Os dados foram exportados com sucesso para:\n{filepath}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, "Erro na Exportação", 
                f"Ocorreu um erro ao exportar os dados:\n{str(e)}"
            )
    
    @Slot()
    def show_context_menu(self, position):
        """Exibe o menu de contexto"""
        # Verificar se há item selecionado
        selected_data = self.get_selected_data()
        if not selected_data:
            return
        
        menu = QMenu(self)
        
        # Opção para copiar
        copy_action = QAction("Copiar", self)
        copy_action.triggered.connect(self.copy_selected_data)
        menu.addAction(copy_action)
        
        # Adicionar outras opções conforme necessário
        menu.exec(self.table.viewport().mapToGlobal(position))
    
    @Slot()
    def copy_selected_data(self):
        """Copia os dados selecionados para a área de transferência"""
        selected_data = self.get_selected_data()
        if not selected_data:
            return
        
        # Construir texto para copiar
        text = "\t".join([title for _, title in self.columns]) + "\n"
        text += "\t".join([str(selected_data.get(name, "")) for name, _ in self.columns])
        
        # Copiar para a área de transferência
        QApplication.clipboard().setText(text)
    
    @Slot()
    def on_selection_changed(self):
        """Chamado quando a seleção na tabela muda"""
        selected_data = self.get_selected_data()
        if selected_data:
            self.itemSelected.emit(selected_data)
    
    @Slot()
    def on_double_click(self):
        """Chamado quando um item da tabela é clicado duas vezes"""
        selected_data = self.get_selected_data()
        if selected_data:
            self.doubleClicked.emit(selected_data)
    
    def clear(self):
        """Limpa todos os dados da tabela"""
        self.data = []
        self.table.setRowCount(0)
    
    def get_all_data(self) -> List[Dict[str, Any]]:
        """Retorna todos os dados da tabela"""
        return self.data
    
    def select_by_id(self, id_value):
        """Seleciona uma linha pelo ID (requer id_column definido)"""
        if not self.id_column:
            return
        
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)  # Qualquer item da linha serve
            if item:
                data = item.data(Qt.ItemDataRole.UserRole)
                if data and data.get(self.id_column) == id_value:
                    self.table.selectRow(row)
                    return