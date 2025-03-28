#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                              QListWidgetItem, QLineEdit, QLabel, QPushButton,
                              QMenu, QAction, QApplication)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from typing import List, Dict, Any, Optional, Callable, Union

class FilterableListWidget(QWidget):
    """Widget de lista com recurso de filtragem"""
    
    # Sinais
    itemSelected = Signal(object)  # Emitido quando um item é selecionado
    doubleClicked = Signal(object)  # Emitido quando um item é clicado duas vezes
    
    def __init__(self, parent=None, items=None, filterable=True, 
                 display_key=None, filter_keys=None):
        """
        Inicializa o widget de lista filtrável
        
        Args:
            parent: Widget pai
            items: Lista de itens (strings ou dicionários)
            filterable: Se a lista pode ser filtrada
            display_key: Chave a ser usada para exibição (se itens são dicionários)
            filter_keys: Lista de chaves para filtrar (se itens são dicionários)
        """
        super().__init__(parent)
        
        self.items = items or []
        self.filterable = filterable
        self.display_key = display_key
        self.filter_keys = filter_keys or []
        
        # Item formatter (função que recebe o item e retorna texto para exibição)
        self.item_formatter = None
        
        self.init_ui()
        
        # Preencher a lista se já tiver itens
        if items:
            self.set_items(items)
    
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Barra de filtro (opcional)
        if self.filterable:
            filter_layout = QHBoxLayout()
            
            # Label
            filter_label = QLabel("Filtrar:")
            filter_layout.addWidget(filter_label)
            
            # Input de filtro
            self.filter_input = QLineEdit()
            self.filter_input.setPlaceholderText("Digite para filtrar...")
            self.filter_input.textChanged.connect(self.apply_filter)
            filter_layout.addWidget(self.filter_input)
            
            # Botão para limpar filtro
            clear_button = QPushButton()
            clear_button.setIcon(QIcon.fromTheme("edit-clear"))
            clear_button.setToolTip("Limpar filtro")
            clear_button.clicked.connect(self.clear_filter)
            filter_layout.addWidget(clear_button)
            
            layout.addLayout(filter_layout)
        
        # Lista
        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        self.list_widget.itemDoubleClicked.connect(self.on_double_click)
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.list_widget)
    
    def set_items(self, items):
        """Define os itens da lista"""
        self.items = items
        self.reload_list()
    
    def reload_list(self):
        """Recarrega os itens na lista"""
        self.list_widget.clear()
        
        # Aplicar filtro se houver
        filtered_items = self.apply_filter()
        
        for item in filtered_items:
            # Criar item da lista
            list_item = QListWidgetItem()
            
            # Definir texto com base no tipo do item
            if isinstance(item, dict) and self.display_key:
                display_text = item.get(self.display_key, "")
            elif self.item_formatter:
                display_text = self.item_formatter(item)
            else:
                display_text = str(item)
            
            list_item.setText(display_text)
            
            # Armazenar dados originais
            list_item.setData(Qt.ItemDataRole.UserRole, item)
            
            # Adicionar à lista
            self.list_widget.addItem(list_item)
    
    def get_selected_item(self):
        """Retorna o item selecionado"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return None
        
        return selected_items[0].data(Qt.ItemDataRole.UserRole)
    
    def set_item_formatter(self, formatter: Callable[[Any], str]):
        """
        Define um formatador para exibição dos itens
        
        Args:
            formatter: Função que recebe o item e retorna texto para exibição
        """
        self.item_formatter = formatter
        # Recarregar a lista para aplicar o formatador
        if self.items:
            self.reload_list()
    
    @Slot()
    def apply_filter(self) -> List:
        """
        Aplica o filtro atual e retorna os itens filtrados
        
        Returns:
            Lista de itens filtrados
        """
        if not self.filterable or not hasattr(self, 'filter_input'):
            return self.items
        
        filter_text = self.filter_input.text().lower() if self.filter_input else ""
        
        if not filter_text:
            filtered_items = self.items
        else:
            filtered_items = []
            
            for item in self.items:
                # Filtrar com base no tipo do item
                if isinstance(item, dict):
                    # Para dicionários, verificar nas chaves especificadas
                    if self.filter_keys:
                        for key in self.filter_keys:
                            if key in item and filter_text in str(item[key]).lower():
                                filtered_items.append(item)
                                break
                    elif self.display_key:
                        # Se não tem filter_keys mas tem display_key, usar esta
                        if filter_text in str(item.get(self.display_key, "")).lower():
                            filtered_items.append(item)
                    else:
                        # Verificar em todas as chaves se não especificado
                        for value in item.values():
                            if filter_text in str(value).lower():
                                filtered_items.append(item)
                                break
                else:
                    # Para outros tipos, verificar na representação string
                    if filter_text in str(item).lower():
                        filtered_items.append(item)
        
        # Se estiver recarregando a lista, atualizar os itens
        if self.sender() == self.filter_input:
            self.list_widget.clear()
            
            for item in filtered_items:
                # Criar item da lista
                list_item = QListWidgetItem()
                
                # Definir texto com base no tipo do item
                if isinstance(item, dict) and self.display_key:
                    display_text = item.get(self.display_key, "")
                elif self.item_formatter:
                    display_text = self.item_formatter(item)
                else:
                    display_text = str(item)
                
                list_item.setText(display_text)
                
                # Armazenar dados originais
                list_item.setData(Qt.ItemDataRole.UserRole, item)
                
                # Adicionar à lista
                self.list_widget.addItem(list_item)
        
        return filtered_items
    
    @Slot()
    def clear_filter(self):
        """Limpa o filtro atual"""
        if hasattr(self, 'filter_input'):
            self.filter_input.clear()
    
    @Slot()
    def on_selection_changed(self):
        """Chamado quando a seleção na lista muda"""
        selected_item = self.get_selected_item()
        if selected_item is not None:
            self.itemSelected.emit(selected_item)
    
    @Slot()
    def on_double_click(self, item):
        """Chamado quando um item da lista é clicado duas vezes"""
        data = item.data(Qt.ItemDataRole.UserRole)
        self.doubleClicked.emit(data)
    
    @Slot()
    def show_context_menu(self, position):
        """Exibe o menu de contexto"""
        # Verificar se há item selecionado
        selected_item = self.get_selected_item()
        if selected_item is None:
            return
        
        menu = QMenu(self)
        
        # Opção para copiar
        copy_action = QAction("Copiar", self)
        copy_action.triggered.connect(self.copy_selected_item)
        menu.addAction(copy_action)
        
        # Adicionar outras opções conforme necessário
        menu.exec(self.list_widget.viewport().mapToGlobal(position))
    
    @Slot()
    def copy_selected_item(self):
        """Copia o item selecionado para a área de transferência"""
        selected_item = self.get_selected_item()
        if selected_item is None:
            return
        
        # Construir texto para copiar
        if isinstance(selected_item, dict) and self.display_key:
            text = str(selected_item.get(self.display_key, ""))
        elif self.item_formatter:
            text = self.item_formatter(selected_item)
        else:
            text = str(selected_item)
        
        # Copiar para a área de transferência
        QApplication.clipboard().setText(text)
    
    def clear(self):
        """Limpa todos os itens da lista"""
        self.items = []
        self.list_widget.clear()
    
    def get_all_items(self):
        """Retorna todos os itens da lista"""
        return self.items