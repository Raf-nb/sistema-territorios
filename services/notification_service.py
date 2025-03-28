#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from models.usuario.usuario import Usuario
from models.usuario.notificacao import Notificacao
from models.designacao.designacao import Designacao
from models.designacao.designacao_predio_vila import DesignacaoPredioVila

class NotificationService:
    """Serviço para gerenciar notificações do sistema"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def verificar_todas_notificacoes(self):
        """Verifica todas as condições que podem gerar notificações"""
        self.verificar_designacoes_proximas_vencimento()
        self.verificar_predios_vilas_proximos_vencimento()
        # Adicionar outras verificações conforme necessário
    
    def verificar_designacoes_proximas_vencimento(self):
        """Verifica designações próximas do vencimento e gera notificações"""
        hoje = datetime.now().date()
        limite = hoje + timedelta(days=5)  # Alerta para 5 dias antes
        
        # Formatar datas para comparação no SQLite
        hoje_str = hoje.strftime('%Y-%m-%d')
        limite_str = limite.strftime('%Y-%m-%d')
        
        # Buscar designações próximas do vencimento
        cursor = self.db_manager.execute(
            "SELECT d.*, t.nome as territorio_nome FROM designacoes d "
            "JOIN territorios t ON d.territorio_id = t.id "
            "WHERE d.status = 'ativo' AND d.data_devolucao BETWEEN ? AND ? "
            "ORDER BY d.data_devolucao",
            (hoje_str, limite_str)
        )
        
        if cursor:
            designacoes = cursor.fetchall()
            
            # Buscar usuários gestores e administradores
            usuarios = [u for u in Usuario.get_ativos(self.db_manager) 
                       if u.nivel_permissao >= Usuario.NIVEL_GESTOR]
            
            # Gerar notificações para cada designação
            for designacao in designacoes:
                dias_restantes = (datetime.strptime(designacao['data_devolucao'], '%Y-%m-%d').date() - hoje).days
                
                titulo = f"Designação próxima do vencimento: {designacao['territorio_nome']}"
                mensagem = (f"A designação do território '{designacao['territorio_nome']}' "
                          f"vence em {dias_restantes} dias ({designacao['data_devolucao']}).")
                
                # Notificar todos os gestores e administradores
                for usuario in usuarios:
                    # Verificar se já existe notificação similar não lida
                    cursor = self.db_manager.execute(
                        "SELECT id FROM notificacoes "
                        "WHERE usuario_id = ? AND entidade = 'designacao' AND entidade_id = ? "
                        "AND status = ? AND tipo = ?",
                        (usuario.id, designacao['id'], Notificacao.STATUS_NAO_LIDA, Notificacao.TIPO_ALERTA)
                    )
                    
                    if cursor and not cursor.fetchone():
                        # Criar notificação
                        Notificacao.criar(
                            self.db_manager,
                            usuario.id,
                            Notificacao.TIPO_ALERTA,
                            titulo,
                            mensagem,
                            None,  # link
                            "designacao",
                            designacao['id']
                        )
    
# Continuação do services/notification_service.py
    def verificar_predios_vilas_proximos_vencimento(self):
        """Verifica designações de prédios/vilas próximas do vencimento"""
        hoje = datetime.now().date()
        limite = hoje + timedelta(days=5)  # Alerta para 5 dias antes
        
        # Formatar datas para comparação no SQLite
        hoje_str = hoje.strftime('%Y-%m-%d')
        limite_str = limite.strftime('%Y-%m-%d')
        
        # Buscar designações próximas do vencimento
        cursor = self.db_manager.execute(
            "SELECT d.*, i.nome as imovel_nome, i.numero, i.tipo "
            "FROM designacoes_predios_vilas d "
            "JOIN imoveis i ON d.imovel_id = i.id "
            "WHERE d.status = 'ativo' AND d.data_devolucao BETWEEN ? AND ? "
            "ORDER BY d.data_devolucao",
            (hoje_str, limite_str)
        )
        
        if cursor:
            designacoes = cursor.fetchall()
            
            # Buscar usuários gestores e administradores
            usuarios = [u for u in Usuario.get_ativos(self.db_manager) 
                       if u.nivel_permissao >= Usuario.NIVEL_GESTOR]
            
            # Gerar notificações para cada designação
            for designacao in designacoes:
                dias_restantes = (datetime.strptime(designacao['data_devolucao'], '%Y-%m-%d').date() - hoje).days
                
                nome_imovel = designacao['imovel_nome'] or f"Nº {designacao['numero']}"
                tipo_imovel = designacao['tipo'].capitalize()
                
                titulo = f"Designação próxima do vencimento: {nome_imovel}"
                mensagem = (f"A designação do {tipo_imovel} '{nome_imovel}' "
                          f"vence em {dias_restantes} dias ({designacao['data_devolucao']}).")
                
                # Notificar todos os gestores e administradores
                for usuario in usuarios:
                    # Verificar se já existe notificação similar não lida
                    cursor = self.db_manager.execute(
                        "SELECT id FROM notificacoes "
                        "WHERE usuario_id = ? AND entidade = 'designacao_predios_vilas' AND entidade_id = ? "
                        "AND status = ? AND tipo = ?",
                        (usuario.id, designacao['id'], Notificacao.STATUS_NAO_LIDA, Notificacao.TIPO_ALERTA)
                    )
                    
                    if cursor and not cursor.fetchone():
                        # Criar notificação
                        Notificacao.criar(
                            self.db_manager,
                            usuario.id,
                            Notificacao.TIPO_ALERTA,
                            titulo,
                            mensagem,
                            None,  # link
                            "designacao_predios_vilas",
                            designacao['id']
                        )
    
    def criar_notificacao_para_usuario(self, usuario_id: int, tipo: str, titulo: str, 
                                      mensagem: str, link: str = None, entidade: str = None, 
                                      entidade_id: int = None) -> bool:
        """Cria uma notificação para um usuário específico"""
        return Notificacao.criar(
            self.db_manager,
            usuario_id,
            tipo,
            titulo,
            mensagem,
            link,
            entidade,
            entidade_id
        )
    
    def criar_notificacao_para_todos(self, tipo: str, titulo: str, 
                                    mensagem: str, link: str = None, entidade: str = None, 
                                    entidade_id: int = None) -> bool:
        """Cria uma notificação para todos os usuários ativos"""
        return Notificacao.criar_para_todos(
            self.db_manager,
            tipo,
            titulo,
            mensagem,
            link,
            entidade,
            entidade_id
        )
    
    def marcar_notificacao_como_lida(self, notificacao_id: int) -> bool:
        """Marca uma notificação como lida"""
        notificacao = Notificacao.get_by_id(self.db_manager, notificacao_id)
        if notificacao:
            return notificacao.marcar_como_lida(self.db_manager)
        return False
    
    def arquivar_notificacao(self, notificacao_id: int) -> bool:
        """Arquiva uma notificação"""
        notificacao = Notificacao.get_by_id(self.db_manager, notificacao_id)
        if notificacao:
            return notificacao.arquivar(self.db_manager)
        return False
    
    def get_notificacoes_nao_lidas(self, usuario_id: int) -> List[Dict]:
        """Obtém as notificações não lidas de um usuário"""
        return Notificacao.get_by_usuario(self.db_manager, usuario_id, apenas_nao_lidas=True)
    
    def get_total_notificacoes_nao_lidas(self, usuario_id: int) -> int:
        """Obtém o total de notificações não lidas de um usuário"""
        notificacoes = self.get_notificacoes_nao_lidas(usuario_id)
        return len(notificacoes)