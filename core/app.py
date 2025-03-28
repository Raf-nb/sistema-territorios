#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe principal da aplicação que inicializa e gerencia os componentes do sistema.
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream, Qt
from PySide6.QtGui import QIcon

from database.db_manager import DatabaseManager
from views.main_window import MainWindow
from utils.config_reader import get_config

class App:
    """Classe principal da aplicação Sistema de Controle de Territórios."""
    
    def __init__(self):
        """Inicializa a aplicação."""
        self.app = None
        self.db_manager = None
        self.main_window = None
        self.config = get_config()
    
    def setup_database(self):
        """Inicializa o banco de dados."""
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database', 'territorios.db')
        self.db_manager = DatabaseManager(db_path)
        self.db_manager.setup_database()
        return self.db_manager
    
    def setup_app_style(self):
        """Configura o estilo visual da aplicação."""
        self.app.setStyle("Fusion")
        
        # Aqui poderia ser implementado um sistema de temas com arquivo CSS
        # style_file = QFile(":/styles/default.css")
        # if style_file.open(QFile.ReadOnly | QFile.Text):
        #     stream = QTextStream(style_file)
        #     self.app.setStyleSheet(stream.readAll())
    
    def run(self):
        """Executa a aplicação."""
        # Cria a aplicação
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Sistema de Controle de Territórios")
        self.app.setOrganizationName("Controle de Territórios")
        self.app.setOrganizationDomain("controleterritorios.org")
        
        # Configura estilo visual
        self.setup_app_style()
        
        # Inicializa o banco de dados
        self.db_manager = self.setup_database()
        
        # Cria a janela principal
        self.main_window = MainWindow(self.db_manager)
        self.main_window.show()
        
        # Inicia o loop de eventos
        return self.app.exec()

def main():
    """Função principal que inicializa e executa a aplicação."""
    app = App()
    sys.exit(app.run())

if __name__ == "__main__":
    main()