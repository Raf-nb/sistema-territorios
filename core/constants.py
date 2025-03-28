#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constantes globais utilizadas em toda a aplicação.
"""

# Tipos de imóveis
class TipoImovel:
    RESIDENCIAL = "residencial"
    COMERCIAL = "comercial"
    PREDIO = "predio"
    VILA = "vila"
    
    @classmethod
    def todos(cls):
        return [cls.RESIDENCIAL, cls.COMERCIAL, cls.PREDIO, cls.VILA]
    
    @classmethod
    def simples(cls):
        return [cls.RESIDENCIAL, cls.COMERCIAL]
    
    @classmethod
    def complexos(cls):
        return [cls.PREDIO, cls.VILA]

# Status de designação
class StatusDesignacao:
    ATIVO = "ativo"
    CONCLUIDO = "concluido"
    
    @classmethod
    def todos(cls):
        return [cls.ATIVO, cls.CONCLUIDO]

# Tipos de portaria
class TipoPortaria:
    VINTE_QUATRO_HORAS = "24-horas"
    ELETRONICA = "eletronica"
    DIURNA = "diurna"
    SEM_PORTARIA = "sem-portaria"
    OUTRO = "outro"
    
    @classmethod
    def todos(cls):
        return [
            cls.VINTE_QUATRO_HORAS,
            cls.ELETRONICA, 
            cls.DIURNA, 
            cls.SEM_PORTARIA, 
            cls.OUTRO
        ]
    
    @classmethod
    def display_names(cls):
        return {
            cls.VINTE_QUATRO_HORAS: "24 horas",
            cls.ELETRONICA: "Eletrônica",
            cls.DIURNA: "Diurna",
            cls.SEM_PORTARIA: "Sem Portaria",
            cls.OUTRO: "Outro"
        }

# Tipos de acesso
class TipoAcesso:
    FACIL = "facil"
    RESTRITO = "restrito"
    INTERFONE = "interfone"
    DIFICIL = "dificil"
    
    @classmethod
    def todos(cls):
        return [cls.FACIL, cls.RESTRITO, cls.INTERFONE, cls.DIFICIL]
    
    @classmethod
    def display_names(cls):
        return {
            cls.FACIL: "Fácil (Sem Restrições)",
            cls.RESTRITO: "Restrito (Com Autorização)",
            cls.INTERFONE: "Via Interfone",
            cls.DIFICIL: "Difícil"
        }

# Resultados de atendimento
class ResultadoAtendimento:
    POSITIVO = "positivo"
    OCUPANTE_AUSENTE = "ocupante-ausente"
    RECUSOU = "recusou-atendimento"
    VISITADO = "apenas-visitado"
    
    @classmethod
    def todos(cls):
        return [
            cls.POSITIVO, 
            cls.OCUPANTE_AUSENTE, 
            cls.RECUSOU, 
            cls.VISITADO
        ]
    
    @classmethod
    def display_names(cls):
        return {
            cls.POSITIVO: "Positivo",
            cls.OCUPANTE_AUSENTE: "Ocupante Ausente",
            cls.RECUSOU: "Recusou Atendimento",
            cls.VISITADO: "Apenas Visitado"
        }

# Tipos de notificação
class TipoNotificacao:
    INFO = "info"
    ALERTA = "alerta"
    ERRO = "erro"
    
    @classmethod
    def todos(cls):
        return [cls.INFO, cls.ALERTA, cls.ERRO]

# Status de notificação
class StatusNotificacao:
    NAO_LIDA = "nao_lida"
    LIDA = "lida"
    ARQUIVADA = "arquivada"
    
    @classmethod
    def todos(cls):
        return [cls.NAO_LIDA, cls.LIDA, cls.ARQUIVADA]

# Tipos de relatório
class TipoRelatorio:
    ATENDIMENTOS = "atendimentos"
    TERRITORIOS = "territorios"
    DESIGNACOES = "designacoes"
    PREDIOS_VILAS = "predios_vilas"
    
    @classmethod
    def todos(cls):
        return [
            cls.ATENDIMENTOS, 
            cls.TERRITORIOS, 
            cls.DESIGNACOES, 
            cls.PREDIOS_VILAS
        ]
    
    @classmethod
    def display_names(cls):
        return {
            cls.ATENDIMENTOS: "Relatório de Atendimentos",
            cls.TERRITORIOS: "Relatório de Territórios",
            cls.DESIGNACOES: "Relatório de Designações",
            cls.PREDIOS_VILAS: "Relatório de Prédios e Vilas"
        }

# Tipos de gráfico
class TipoGrafico:
    BARRAS = "barras"
    PIZZA = "pizza"
    LINHA = "linha"
    AREA = "area"
    
    @classmethod
    def todos(cls):
        return [cls.BARRAS, cls.PIZZA, cls.LINHA, cls.AREA]
    
    @classmethod
    def display_names(cls):
        return {
            cls.BARRAS: "Gráfico de Barras",
            cls.PIZZA: "Gráfico de Pizza",
            cls.LINHA: "Gráfico de Linha",
            cls.AREA: "Gráfico de Área"
        }

# Níveis de permissão
class NivelPermissao:
    BASICO = 1
    GESTOR = 2
    ADMIN = 3
    
    @classmethod
    def todos(cls):
        return [cls.BASICO, cls.GESTOR, cls.ADMIN]
    
    @classmethod
    def display_names(cls):
        return {
            cls.BASICO: "Usuário Básico",
            cls.GESTOR: "Gestor",
            cls.ADMIN: "Administrador"
        }

# Tipos de log de atividade
class TipoLogAtividade:
    LOGIN = "login"
    LOGOUT = "logout"
    CRIAR = "criar"
    EDITAR = "editar"
    EXCLUIR = "excluir"
    VISUALIZAR = "visualizar"
    
    @classmethod
    def todos(cls):
        return [
            cls.LOGIN, 
            cls.LOGOUT, 
            cls.CRIAR, 
            cls.EDITAR, 
            cls.EXCLUIR, 
            cls.VISUALIZAR
        ]