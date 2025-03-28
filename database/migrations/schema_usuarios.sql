-- Schema para as tabelas de usuários, log de atividades e notificações
-- Extensão do schema principal do Sistema de Controle de Territórios

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    nivel_permissao INTEGER NOT NULL DEFAULT 1, -- 1: básico, 2: gestor, 3: admin
    ativo INTEGER NOT NULL DEFAULT 1,
    ultima_atividade TEXT,
    preferencias TEXT, -- Preferências em formato JSON
    data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de perfis de usuário (informações adicionais)
CREATE TABLE IF NOT EXISTS usuario_perfis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    telefone TEXT,
    cargo TEXT,
    biografia TEXT,
    avatar_path TEXT,
    tema_preferido TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela de log de atividades
CREATE TABLE IF NOT EXISTS log_atividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    tipo_acao TEXT NOT NULL, -- 'login', 'logout', 'criar', 'editar', 'excluir', 'visualizar'
    descricao TEXT NOT NULL,
    data_hora TEXT DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    entidade TEXT, -- tipo de entidade (território, designação, etc.)
    entidade_id INTEGER, -- id da entidade, se aplicável
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela de notificações
CREATE TABLE IF NOT EXISTS notificacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    tipo TEXT NOT NULL, -- 'info', 'alerta', 'erro'
    titulo TEXT NOT NULL,
    mensagem TEXT NOT NULL,
    status TEXT NOT NULL, -- 'nao_lida', 'lida', 'arquivada'
    data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
    data_leitura TEXT,
    link TEXT, -- link/ação relacionada à notificação
    entidade TEXT, -- tipo de entidade relacionada
    entidade_id INTEGER, -- id da entidade, se aplicável
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela para controle de sessões
CREATE TABLE IF NOT EXISTS sessoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    ip_address TEXT,
    user_agent TEXT,
    data_inicio TEXT DEFAULT CURRENT_TIMESTAMP,
    data_expiracao TEXT NOT NULL,
    ativa INTEGER DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela para configurações personalizadas de usuários
CREATE TABLE IF NOT EXISTS usuario_configuracoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL UNIQUE,
    chave TEXT NOT NULL,
    valor TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Índices para consultas frequentes
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_nivel_permissao ON usuarios(nivel_permissao);

CREATE INDEX IF NOT EXISTS idx_log_usuario_id ON log_atividades(usuario_id);
CREATE INDEX IF NOT EXISTS idx_log_data_hora ON log_atividades(data_hora);
CREATE INDEX IF NOT EXISTS idx_log_tipo_acao ON log_atividades(tipo_acao);

CREATE INDEX IF NOT EXISTS idx_notificacoes_usuario_id ON notificacoes(usuario_id);
CREATE INDEX IF NOT EXISTS idx_notificacoes_status ON notificacoes(status);
CREATE INDEX IF NOT EXISTS idx_notificacoes_tipo ON notificacoes(tipo);

CREATE INDEX IF NOT EXISTS idx_sessoes_token ON sessoes(token);
CREATE INDEX IF NOT EXISTS idx_sessoes_usuario_id ON sessoes(usuario_id);
CREATE INDEX IF NOT EXISTS idx_sessoes_ativa ON sessoes(ativa);

CREATE INDEX IF NOT EXISTS idx_usuario_configuracoes_usuario_chave ON usuario_configuracoes(usuario_id, chave);