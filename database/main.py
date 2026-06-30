from config import Config
import sqlite3
import os



def init_db():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Tabela funcionarios
    cursor.execute('''CREATE TABLE IF NOT EXISTS funcionarios (
        id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT,
        email TEXT,
        senha TEXT,
        telefone TEXT,
        cpf TEXT NOT NULL UNIQUE    
    )''')
    
    # Tabela empresas
    cursor.execute('''CREATE TABLE IF NOT EXISTS empresas (
        id_empresa INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT,
        endereco TEXT,
        email TEXT,
        senha TEXT,
        telefone TEXT,
        cnpj TEXT NOT NULL UNIQUE
    )''')
    
    # Tabela competencias
    cursor.execute('''CREATE TABLE IF NOT EXISTS competencias (
        id_competencia INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT
    )''')
    
    # Tabela funcionario_competencias
    cursor.execute('''CREATE TABLE IF NOT EXISTS funcionario_competencias (
        id_funcionario INTEGER,
        id_competencia INTEGER,
        FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario) ON DELETE CASCADE,
        FOREIGN KEY (id_competencia) REFERENCES competencias (id_competencia) ON DELETE CASCADE
    )''')
    
    # Tabela questionario
    cursor.execute('''CREATE TABLE IF NOT EXISTS respostas_questionario (
        id_resposta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_funcionario INTEGER,
        cidade TEXT,
        estado TEXT,
        formacao TEXT, 
        curso TEXT,
        instituicao TEXT, 
        ano_conclusao INTEGER,
        ultimo_cargo TEXT,
        ultima_empresa TEXT,
        tempo_experiencia TEXT, 
        data_preenchimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario) ON DELETE CASCADE
    )''')

    # Tabela vagas
    cursor.execute('''CREATE TABLE IF NOT EXISTS vagas (
        id_vaga INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descricao TEXT,
        salario REAL,
        cidade TEXT,
        regime TEXT,
        status TEXT DEFAULT 'ativa',
        data_publicacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        id_empresa INTEGER ,
        FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa)
    )''')
    
    # Tabela vaga_competencias
    cursor.execute('''CREATE TABLE IF NOT EXISTS vaga_competencias (
        id_vaga INTEGER,
        id_competencia INTEGER ,
        PRIMARY KEY (id_vaga, id_competencia),
        FOREIGN KEY (id_vaga) REFERENCES vagas (id_vaga) ON DELETE CASCADE,
        FOREIGN KEY (id_competencia) REFERENCES competencias (id_competencia) ON DELETE CASCADE
    )''')
    # Tabela candidaturas
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidaturas (
        id_candidatura INTEGER PRIMARY KEY AUTOINCREMENT,
        id_funcionario INTEGER,
        id_vaga INTEGER,
        data_candidatura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pendente',
        FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario) ON DELETE CASCADE,
        FOREIGN KEY (id_vaga) REFERENCES vagas (id_vaga) ON DELETE CASCADE,
        UNIQUE(id_funcionario, id_vaga)
    )''')

    # Tabela freelancers
    cursor.execute('''CREATE TABLE IF NOT EXISTS freelancers (
        id_freelancer INTEGER PRIMARY KEY AUTOINCREMENT,
        id_funcionario INTEGER NOT NULL,
        profissao TEXT,
        servico_oferecido TEXT,
        preco_medio REAL,
        disponibilidade TEXT DEFAULT 'disponivel',
        total_avaliacoes INTEGER DEFAULT 0,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_funcionario) REFERENCES funcionarios (id_funcionario) ON DELETE CASCADE
    )''')
    
    cursor.execute('''
        CREATE TABLE if not exists contratacoes(
        id_contratacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_freelancer INTEGER NOT NULL,
        id_contratante INTEGER NOT NULL,
        tipo_contratante TEXT NOT NULL DEFAULT 'empresa'
            CHECK(tipo_contratante IN ('empresa','funcionario')),
        data_contratacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pendente'
            CHECK(status IN ('pendente','aceito','recusado','concluido','cancelado')),
        data_conclusao TIMESTAMP,
        FOREIGN KEY (id_freelancer)
            REFERENCES freelancers(id_freelancer)
            ON DELETE CASCADE
        );
    ''')
    # Tabela avaliacoes (avaliações de freelancers)
    cursor.execute('''CREATE TABLE IF NOT EXISTS avaliacoes (
        id_avaliacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_freelancer INTEGER,
        id_contratante INTEGER,
        tipo_contratante TEXT DEFAULT NULL,
        nota INTEGER CHECK(nota >= 1 AND nota <= 5),
        comentario TEXT,
        data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_freelancer) REFERENCES freelancers (id_freelancer) ON DELETE CASCADE
    )''')

    # Tabela notificacoes (alertas na tela)
    cursor.execute('''CREATE TABLE IF NOT EXISTS notificacoes (
        id_notificacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        mensagem TEXT NOT NULL,
        tipo TEXT NOT NULL,
        id_referencia INTEGER,
        lida INTEGER DEFAULT 0,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS salas_chat (
            id_sala INTEGER PRIMARY KEY AUTOINCREMENT,
            id_candidatura INTEGER NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_candidatura) REFERENCES candidaturas (id_candidatura) ON DELETE CASCADE,
            UNIQUE(id_candidatura)
     ) ''')
    # Tabela mensagens do chat
    cursor.execute('''CREATE TABLE IF NOT EXISTS mensagens_chat (
        id_mensagem INTEGER PRIMARY KEY AUTOINCREMENT,
        id_candidatura INTEGER NOT NULL,
        id_remetente INTEGER NOT NULL,
        tipo_remetente TEXT NOT NULL CHECK(tipo_remetente IN ('empresa', 'funcionario')),
        mensagem TEXT NOT NULL,
        enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_candidatura) REFERENCES candidaturas (id_candidatura) ON DELETE CASCADE
    )''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()