-- Schema para as tabelas de relatórios e exportações
-- Extensão do schema principal do Sistema de Controle de Territórios

-- Tabela para armazenar relatórios personalizáveis
CREATE TABLE IF NOT EXISTS relatorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    tipo TEXT NOT NULL, -- 'atendimentos', 'territorios', 'designacoes', 'predios_vilas'
    filtros TEXT, -- Filtros em formato JSON
    compartilhado INTEGER DEFAULT 0, -- Se o relatório é compartilhado com outros usuários
    usuario_id INTEGER,
    data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
    ultima_execucao TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela para armazenar os resultados de relatórios (cache)
CREATE TABLE IF NOT EXISTS relatorio_resultados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relatorio_id INTEGER NOT NULL,
    resultados TEXT NOT NULL, -- Resultados em formato JSON
    data_geracao TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (relatorio_id) REFERENCES relatorios(id) ON DELETE CASCADE
);

-- Tabela para armazenar exportações de relatórios
CREATE TABLE IF NOT EXISTS relatorio_exportacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relatorio_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    formato TEXT NOT NULL, -- 'pdf', 'csv', 'excel'
    caminho_arquivo TEXT NOT NULL,
    data_exportacao TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (relatorio_id) REFERENCES relatorios(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela para armazenar agendamentos de relatórios
CREATE TABLE IF NOT EXISTS relatorio_agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relatorio_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    frequencia TEXT NOT NULL, -- 'diario', 'semanal', 'mensal'
    dia_semana INTEGER, -- 0-6 para relatórios semanais
    dia_mes INTEGER, -- 1-31 para relatórios mensais
    hora TEXT NOT NULL, -- HH:MM
    ativo INTEGER DEFAULT 1,
    enviar_email INTEGER DEFAULT 0,
    email_destinatarios TEXT,
    ultima_execucao TEXT,
    proxima_execucao TEXT,
    FOREIGN KEY (relatorio_id) REFERENCES relatorios(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela para modelos de relatórios (templates)
CREATE TABLE IF NOT EXISTS relatorio_modelos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    tipo TEXT NOT NULL, -- 'atendimentos', 'territorios', 'designacoes', 'predios_vilas'
    filtros_padrao TEXT, -- Filtros padrão em formato JSON
    template TEXT, -- Template HTML ou outro formato
    sistema INTEGER DEFAULT 0, -- Se é um modelo do sistema (não pode ser excluído)
    usuario_id INTEGER,
    data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela para compartilhamento de relatórios
CREATE TABLE IF NOT EXISTS relatorio_compartilhamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relatorio_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL, -- Usuário com quem o relatório é compartilhado
    permissao TEXT DEFAULT 'leitura', -- 'leitura', 'edicao'
    data_compartilhamento TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (relatorio_id) REFERENCES relatorios(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Índices para consultas frequentes
CREATE INDEX IF NOT EXISTS idx_relatorios_usuario_id ON relatorios(usuario_id);
CREATE INDEX IF NOT EXISTS idx_relatorios_tipo ON relatorios(tipo);
CREATE INDEX IF NOT EXISTS idx_relatorios_compartilhado ON relatorios(compartilhado);
CREATE INDEX IF NOT EXISTS idx_relatorios_ultima_execucao ON relatorios(ultima_execucao);

CREATE INDEX IF NOT EXISTS idx_relatorio_resultados_relatorio_id ON relatorio_resultados(relatorio_id);
CREATE INDEX IF NOT EXISTS idx_relatorio_resultados_data_geracao ON relatorio_resultados(data_geracao);

CREATE INDEX IF NOT EXISTS idx_relatorio_exportacoes_relatorio_id ON relatorio_exportacoes(relatorio_id);
CREATE INDEX IF NOT EXISTS idx_relatorio_exportacoes_usuario_id ON relatorio_exportacoes(usuario_id);

CREATE INDEX IF NOT EXISTS idx_relatorio_agendamentos_relatorio_id ON relatorio_agendamentos(relatorio_id);
CREATE INDEX IF NOT EXISTS idx_relatorio_agendamentos_usuario_id ON relatorio_agendamentos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_relatorio_agendamentos_ativo ON relatorio_agendamentos(ativo);
CREATE INDEX IF NOT EXISTS idx_relatorio_agendamentos_proxima_execucao ON relatorio_agendamentos(proxima_execucao);

CREATE INDEX IF NOT EXISTS idx_relatorio_compartilhamentos_relatorio_id ON relatorio_compartilhamentos(relatorio_id);
CREATE INDEX IF NOT EXISTS idx_relatorio_compartilhamentos_usuario_id ON relatorio_compartilhamentos(usuario_id);