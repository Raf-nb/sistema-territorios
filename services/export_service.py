#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
from typing import Dict, Any, List, Optional
from datetime import datetime

class ExportService:
    """Serviço para exportar dados do sistema"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def export_to_csv(self, data: List[Dict], headers: List[str], 
                     file_path: str, adicionar_cabecalho: bool = True) -> bool:
        """Exporta dados para um arquivo CSV"""
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Escrever cabeçalho se solicitado
                if adicionar_cabecalho:
                    writer.writerow(headers)
                
                # Escrever dados
                for row in data:
                    writer.writerow([row.get(h, "") for h in headers])
            
            return True
        except Exception as e:
            print(f"Erro ao exportar para CSV: {e}")
            return False
    
    def export_report_to_csv(self, relatorio_resultados: Dict[str, Any], file_path: str) -> bool:
        """Exporta um relatório para CSV"""
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Adicionar informações do relatório
                writer.writerow([relatorio_resultados["titulo"]])
                writer.writerow([f"Gerado em: {relatorio_resultados['data_geracao']}"])
                writer.writerow([])  # Linha em branco
                
                # Adicionar totais
                writer.writerow(["Resumo"])
                for key, value in relatorio_resultados.get("totais", {}).items():
                    key_display = key.replace("_", " ").capitalize()
                    writer.writerow([key_display, value])
                
                writer.writerow([])  # Linha em branco
                
                # Adicionar dados detalhados com base no tipo de relatório
                if relatorio_resultados["tipo"] == "atendimentos":
                    self._export_atendimentos_data(writer, relatorio_resultados)
                elif relatorio_resultados["tipo"] == "territorios":
                    self._export_territorios_data(writer, relatorio_resultados)
                elif relatorio_resultados["tipo"] == "designacoes":
                    self._export_designacoes_data(writer, relatorio_resultados)
                elif relatorio_resultados["tipo"] == "predios_vilas":
                    self._export_predios_vilas_data(writer, relatorio_resultados)
            
            return True
        except Exception as e:
            print(f"Erro ao exportar relatório para CSV: {e}")
            return False
    
    def _export_atendimentos_data(self, writer, relatorio_resultados):
        """Exporta dados específicos de relatório de atendimentos"""
        dados = relatorio_resultados.get("dados", {})
        
        # Contagem por tipo de imóvel
        if "por_tipo_imovel" in dados:
            writer.writerow(["Atendimentos por Tipo de Imóvel"])
            writer.writerow(["Tipo de Imóvel", "Total de Atendimentos"])
            for tipo, total in dados["por_tipo_imovel"].items():
                writer.writerow([tipo.capitalize(), total])
            writer.writerow([])
        
        # Contagem por território
        if "por_territorio" in dados:
            writer.writerow(["Atendimentos por Território"])
            writer.writerow(["Território", "Total de Atendimentos"])
            for territorio, total in dados["por_territorio"].items():
                writer.writerow([territorio, total])
            writer.writerow([])
        
        # Contagem por mês
        if "por_mes" in dados:
            writer.writerow(["Atendimentos por Mês"])
            writer.writerow(["Mês", "Total de Atendimentos"])
            for mes, total in dados["por_mes"].items():
                writer.writerow([mes, total])
    
    def _export_territorios_data(self, writer, relatorio_resultados):
        """Exporta dados específicos de relatório de territórios"""
        territorios = relatorio_resultados.get("dados", {}).get("territorios", [])
        
        if territorios:
            writer.writerow(["Dados Detalhados por Território"])
            writer.writerow([
                "Território", "Total de Ruas", "Total de Imóveis", 
                "Total de Atendimentos", "Atendimentos Mês Atual", 
                "Cobertura (%)", "Última Visita"
            ])
            
            for t in territorios:
                writer.writerow([
                    t["nome"],
                    t["total_ruas"],
                    t["total_imoveis"],
                    t["total_atendimentos"],
                    t["atendimentos_mes_atual"],
                    t["cobertura_percentual"],
                    t["ultima_visita"] or "Não definida"
                ])
    
    def _export_designacoes_data(self, writer, relatorio_resultados):
        """Exporta dados específicos de relatório de designações"""
        dados = relatorio_resultados.get("dados", {})
        
        # Status de designações
        writer.writerow(["Designações por Status"])
        writer.writerow(["Status", "Total"])
        writer.writerow(["Ativas", relatorio_resultados["totais"].get("ativas", 0)])
        writer.writerow(["Concluídas", relatorio_resultados["totais"].get("concluidas", 0)])
        writer.writerow([])
        
        # Dados por território
        if "por_territorio" in dados:
            writer.writerow(["Designações por Território"])
            writer.writerow(["Território", "Total de Designações"])
            for territorio, total in dados["por_territorio"].items():
                writer.writerow([territorio, total])
            writer.writerow([])
        
        # Dados por mês
        if "por_mes" in dados:
            writer.writerow(["Designações por Mês"])
            writer.writerow(["Mês", "Total de Designações"])
            for mes, total in dados["por_mes"].items():
                writer.writerow([mes, total])
    
    def _export_predios_vilas_data(self, writer, relatorio_resultados):
        """Exporta dados específicos de relatório de prédios e vilas"""
        predios_vilas = relatorio_resultados.get("dados", {}).get("predios_vilas", [])
        
        if predios_vilas:
            writer.writerow(["Dados Detalhados de Prédios e Vilas"])
            writer.writerow([
                "Nome", "Tipo", "Endereço", "Território",
                "Total de Unidades", "Unidades Atendidas",
                "Cobertura (%)", "Designação Ativa"
            ])
            
            for pv in predios_vilas:
                writer.writerow([
                    pv["nome"],
                    pv["tipo"].capitalize(),
                    pv["endereco"],
                    pv["territorio"],
                    pv["total_unidades"],
                    pv["unidades_atendidas"],
                    pv["cobertura_percentual"],
                    "Sim" if pv["designacao_ativa"] else "Não"
                ])