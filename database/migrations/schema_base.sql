-- Schema principal para o banco de dados do Sistema de Controle de Territórios
-- Contém as tabelas fundamentais do sistema

-- Habilitar chaves estrangeiras
PRAGMA foreign_keys = ON;

-- Tabela de territórios
CREATE TABLE IF NOT EXISTS territorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    ultima_visita TEXT,
    data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de ruas
CREATE TABLE IF NOT EXISTS ruas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    territorio_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    FOREIGN KEY (territorio_id) REFERENCES territorios(id) ON DELETE CASCADE
);

-- Tabela de imóveis
CREATE TABLE IF NOT EXISTS imoveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rua_id INTEGER NOT NULL,
    numero TEXT NOT NULL,
    tipo TEXT NOT NULL, -- 'residencial', 'comercial', 'predio', 'vila'
    nome TEXT, -- Nome do edifício (opcional)
    total_unidades INTEGER, -- Total de apartamentos/unidades (para prédios e vilas)
    tipo_portaria TEXT, -- '24-horas', 'eletronica', 'diurna', 'sem-portaria', 'outro'
    tipo_acesso TEXT, -- 'facil', 'restrito', 'interfone', 'dificil'
    observacoes TEXT,
    FOREIGN KEY (rua_id) REFERENCES ruas(id) ON DELETE CASCADE
);

-- Tabela de unidades (apartamentos em prédios ou casas em vilas)
CREATE TABLE IF NOT EXISTS unidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imovel_id INTEGER NOT NULL,
    numero TEXT NOT NULL,
    observacoes TEXT,
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id) ON DELETE CASCADE
);

-- Tabela de saídas de campo
CREATE TABLE IF NOT EXISTS saidas_campo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    data TEXT NOT NULL,
    dia_semana TEXT NOT NULL,
    horario TEXT NOT NULL,
    dirigente TEXT,
    data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de designações de territórios
CREATE TABLE IF NOT EXISTS designacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    territorio_id INTEGER NOT NULL,
    saida_campo_id INTEGER NOT NULL,
    data_designacao TEXT NOT NULL,
    data_devolucao TEXT,
    responsavel TEXT,
    status TEXT DEFAULT 'ativo', -- 'ativo', 'concluido'
    FOREIGN KEY (territorio_id) REFERENCES territorios(id) ON DELETE CASCADE,
    FOREIGN KEY (saida_campo_id) REFERENCES saidas_campo(id) ON DELETE CASCADE
);

-- Tabela de atendimentos
CREATE TABLE IF NOT EXISTS atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imovel_id INTEGER NOT NULL,
    unidade_id INTEGER, -- NULL para imóveis residenciais/comerciais
    data TEXT NOT NULL,
    resultado TEXT, -- 'positivo', 'ocupante-ausente', 'recusou-atendimento', 'apenas-visitado'
    observacoes TEXT,
    data_registro TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id) ON DELETE CASCADE,
    FOREIGN KEY (unidade_id) REFERENCES unidades(id) ON DELETE CASCADE
);

-- Tabela de histórico de trabalho em prédios/vilas
CREATE TABLE IF NOT EXISTS historico_predios_vilas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imovel_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data_registro TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id) ON DELETE CASCADE
);

-- Tabela para designações específicas de prédios/vilas
CREATE TABLE IF NOT EXISTS designacoes_predios_vilas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    imovel_id INTEGER NOT NULL,
    responsavel TEXT NOT NULL,
    saida_campo_id INTEGER NOT NULL,
    data_designacao TEXT NOT NULL,
    data_devolucao TEXT,
    status TEXT DEFAULT 'ativo', -- 'ativo', 'concluido'
    FOREIGN KEY (imovel_id) REFERENCES imoveis(id) ON DELETE CASCADE,
    FOREIGN KEY (saida_campo_id) REFERENCES saidas_campo(id) ON DELETE CASCADE
);

-- Índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_ruas_territorio_id ON ruas(territorio_id);
CREATE INDEX IF NOT EXISTS idx_imoveis_rua_id ON imoveis(rua_id);
CREATE INDEX IF NOT EXISTS idx_imoveis_tipo ON imoveis(tipo);
CREATE INDEX IF NOT EXISTS idx_unidades_imovel_id ON unidades(imovel_id);
CREATE INDEX IF NOT EXISTS idx_designacoes_territorio_id ON designacoes(territorio_id);
CREATE INDEX IF NOT EXISTS idx_designacoes_saida_campo_id ON designacoes(saida_campo_id);
CREATE INDEX IF NOT EXISTS idx_designacoes_status ON designacoes(status);
CREATE INDEX IF NOT EXISTS idx_atendimentos_imovel_id ON atendimentos(imovel_id);
CREATE INDEX IF NOT EXISTS idx_atendimentos_data ON atendimentos(data);
CREATE INDEX IF NOT EXISTS idx_historico_imovel_id ON historico_predios_vilas(imovel_id);
CREATE INDEX IF NOT EXISTS idx_designacoes_predios_vilas_imovel_id ON designacoes_predios_vilas(imovel_id);
CREATE INDEX IF NOT EXISTS idx_designacoes_predios_vilas_status ON designacoes_predios_vilas(status);