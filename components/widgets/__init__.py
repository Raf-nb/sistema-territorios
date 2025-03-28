# components/widgets/__init__.py
"""
Widgets personalizados reutilizáveis
"""
from components.widgets.custom_table import CustomTableWidget
from components.widgets.filterable_list import FilterableListWidget
from components.widgets.status_badge import StatusBadge
from components.widgets.progress_card import ProgressCard

__all__ = [
    'CustomTableWidget', 
    'FilterableListWidget', 
    'StatusBadge', 
    'ProgressCard'
]