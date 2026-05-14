Projeto - Conectar-CE

O **Conectar-CE** é uma plataforma digital centralizada focada em fortalecer o mercado de trabalho na região do Crajubar (Crato, Juazeiro do Norte e Barbalha). O sistema atua como um hub de empregabilidade, digitalizando o "boca a boca" regional e conectando contratantes a trabalhadores 
de forma rápida e gratuita.

## 🚀 Funcionalidades (MVP)
- [ ] Cadastro e Login de usuários.
- [ ] Mural de vagas dinâmico com filtros por cidade (Juazeiro, Crato, Barbalha).
- [ ] Cadastro de perfil profissional para autônomos.
- [ ] Área para empresas/contratantes postarem anúncios.
- [ ] Dashboard simples para gerenciamento de posts.

## Visão Geral

O Vagas Conecta é uma aplicação web desenvolvida em Flask que permite:
    **Funcionários:** Cadastrar-se, preencher perfil profissional com competências, buscar vagas compatíveis e candidatar-se.
    **Empresas:** Cadastrar-se e publicar vagas com requisitos de competências.
    **Sistema de Match:** Calcula automaticamente a compatibilidade entre o perfil do candidato e os requisitos da vaga.

## Funcionalidades
**Para Funcionários:**
    *Cadastro* com autenticação local ou Google OAuth
    Questionário complementar com dados profissionais
    *Seleção* e adição de competências personalizadas
    Listagem de vagas com filtros (busca, salário, empresa)
    *Visualização* de vagas recomendadas por compatibilidade
    Candidatura a vagas com verificação de duplicidade
    *Histórico* de candidaturas
**Para Empresas:**
    Criação de vagas com competências necessárias
    Gestão de vagas publicadas e candidaturas

## TECNOLOGIAS UTILIZADAS 
**Tecnologia| Descrição**
Python 3.x  | Linguagem principal
Flask       | Framework web
SQLite3	    | Banco de dados
Authlib	    | Autenticação OAuth (Google)
HTML5/CSS3	| Interface do usuário
JavaScript	| Interatividade front-end
Jinja2	    | Template engine

## Estrutura do Projeto

vagas-conecta/
│
├── app.py                      # Arquivo principal da aplicação
├── config.py                   # Configurações e variáveis de ambiente
├── .env                        # Variáveis sensíveis (não versionado)
├── requirements.txt            # Dependências do projeto
│
├── database/
│   ├── __init__.py
│   ├── connect.py              # Conexão com banco de dados
│   ├── main.py                 # Inicialização das tabelas
│   └── banco.db                # Arquivo SQLite (gerado)
│
├── CRUDs/
│   ├── __init__.py
│   ├── candidatura.py          # CRUD de candidaturas e match
│   ├── crud_comp.py            # CRUD de competências
│   ├── crud_emp.py             # CRUD de empresas
│   ├── crud_func.py            # CRUD de funcionários
│   ├── crud_quest.py           # CRUD do questionário
│   └── crud_vagas.py           # CRUD de vagas
│
├── models/
│   ├── __init__.py
│   ├── model_comp.py           # Regras de competências
│   ├── model_emp.py            # Regras de empresas
│   ├── model_fun.py            # Regras de funcionários
│   ├── model_quest.py          # Regras do questionário
│   └── model_vagas.py          # Regras de vagas
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Rotas de autenticação
│   ├── google_auth.py          # Rotas OAuth Google
│   ├── home.py                 # Rota inicial
│   ├── questionario.py         # Rotas do questionário
│   └── vagas.py                # Rotas de vagas
│
├── static/
│   ├── css/
│   │   ├── candidatura.css
│   │   ├── homef.css
│   │   ├── index.css
│   │   ├── questionario.css
│   │   └── vagas.css
│   ├── imagem/
│   │   ├── google-icon.png 
│   │   ├── linkedin-icon.png
│   │   ├── image1.jpg
│   │   └── logo.png
│   └── script/
│       ├── emp.js
│       ├── index.js
│       └── questionario.js
│
└── templates/
    ├── index.html              # Página de login/cadastro
    ├── home_func.html          # Home do funcionário
    ├── home_emp.html           # Home da empresa
    ├── questionario.html       # Questionário complementar
    └── vaga/
        ├── candidaturas.html       # Minhas candidaturas
        ├── vagas_listar.html       # Lista de vagas
        ├── vagas_recomendadas.html # Vagas recomendadas
        └── vaga_detalhe.html       # Detalhes da vaga

## BANCO DE DADOS ==============================================================================
**FUNCIONARIOS==================================**
*Coluna	      | Tipo	 | Descrição*
id_funcionario|	INTEGER  |PK Identificador único
nome	      |TEXT	     |Nome completo
email	      |TEXT	     |E-mail (único)
senha	      |TEXT	     |Senha criptografada
telefone	  |TEXT	     |Telefone de contato
cpf	          |TEXT	     |CPF (único)
**EMPRESAS======================================**
*Coluna	      | Tipo	 | Descrição*
id_empresa	|INTEGER  |PK Identificador único
nome	      |TEXT	     |Nome da empresa
cnpj	      |TEXT	     |CNPJ da empresa
email	      |TEXT	     |E-mail da empresa
telefone	  |TEXT	     |Telefone da empresa
senha	      |TEXT	     |Senha da empresa
endereco	  |TEXT	     |Endereço da empresa
**VAGAS========================================**
*Coluna	      | Tipo	 | Descrição*
id_vaga	    |INTEGER  |PK Identificador único
id_empresa	|INTEGER  |FK Identificador da empresa
titulo	    |TEXT	     |Título da vaga
descricao	|TEXT	     |Descrição da vaga
salario	    |REAL        |Salário mínimo da vaga
cidade	    |TEXT	     |Cidade da vaga
regime	    |TEXT	     |Regime de contratação
status	    |TEXT	     |Status da vaga
**COMPETENCIAS===================================**
*Coluna	      | Tipo	 | Descrição*
id_competencia|INTEGER  |PK Identificador único
nome	      |TEXT	     |Nome da competência
**CANDIDATURAS====================================**
*Coluna	      | Tipo	 | Descrição*
id_candidato   |INTEGER  |PK Identificador único
id_vaga	       |INTEGER  |FK Identificador da vaga
id_funcionario |INTEGER  |FK Identificador do funcionário
data	       |TEXT 	 |Data da candidatura
status	    |TEXT	     |Status da candidatura

## Rotas da Aplicação ==============================================================================

*Autenticação (routes/auth.py)*
Rotas                 | Descrição
--------------------- | -------------
/                     | Home - antes do login o index
/login                | login autenticação de usuário
/cadastro/funcionario | Cadastro de funcionário
/cadastro/empresa     | Cadastro de empresa

*Google Auth (routes/google_auth.py)*
Rotas                 | Descrição
--------------------- | -------------
/google-login         | Login com Google
/signin-google        | Redirecionamento após o login

*Home (routes/home.py)*
Rotas                 | Descrição
--------------------- | -------------
/home                 | Home Página inicial pós-login
/logout               | Logout 

*Questionário (routes/questionario.py)*
Rotas                  | Descrição
---------------------  | -------------
/questionario/<id_func>| Página de questionário do funcionário
/salvar_questionario   | Salvar questionário do funcionário

*Vagas (routes/vagas.py)*
Rotas                       | Descrição
---------------------       | -------------
/vagas                      | lista vagas com filtros
/vagas/<id_vaga>            | Detalhes da vaga
/vagas/<id_vaga>/candidatar | candidatar a vaga
/empresa/vaga/criar         | Criar vaga


## Modelos e Regras de Negócio =====================================================================
Arquitetura em 3 Camadas
Routes (rotas) → Models (regras) → CRUDs (banco)

*Validações Principais*

*Funcionário:=========================*
    *Nome:*   | mínimo 3 caracteres
    *E-mail:* | deve conter @
    *Senha:*  | mínimo 6 caracteres
    *CPF:*    | exatamente 11 dígitos
*Empresa:=============================*
    *Nome:*   | mínimo 2 caracteres
    *CNPJ:*   |exatamente 14 dígitos
    *E-mail:* | deve conter @
    *Senha:*  | mínimo 6 caracteres
*Vaga: ===============================*
    *Descrição:*   | mínimo 50 caracteres
    *Salário:*     | não pode ser negativo
    *Competencia:* | Pelo menos uma competência necessária
*Candidatura: ===============================*
    *Condicao:*    |Um funcionário não pode se candidatar duas vezes à mesma vaga


## Interface do Usuário ===========================================================================
*Cores:*      | *codigo*    | *uso*
*Azul escuro* | #05186c   | Headers, botões principais
*Azul medio*  | #488BA8   | Textos sobre escuro
*Azul claro*  | #99E2F2   | Fundo gradiente

**Páginas Disponíveis ================================================**
    *Login/Cadastro (index.html)*          - Página inicial com formulários de acesso
    *Home Funcionário (home_func.html)*    - Dashboard pós-login
    *Questionário (questionario.html)*     - Formulário de perfil profissional
    *Lista de Vagas (vagas_listar.html)*   - Vagas com filtros e match
    *Detalhe da Vaga (vaga_detalhe.html)*  - Informações completas

## Fluxo de Uso ==============================================================================
Fluxo do Funcionário
┌──────────┐   ┌──────────────┐   ┌─────────────┐   ┌──────────┐   ┌──────────────┐
│ Registro │──>│ Questionário │──>│Competências │──>│  Buscar  │──>│ Candidatar-se│
└──────────┘   └──────────────┘   └─────────────┘   │  Vagas   │   └──────────────┘
                                                    └──────────┘
Fluxo da Empresa
┌──────────┐   ┌────────┐   ┌───────────┐   ┌──────────────┐   ┌──────────┐
│ Registro │──>│ Login  │──>│ Criar Vaga │──>│ Selecionar    │──>│ Publicar │
└──────────┘   └────────┘   └───────────┘   │ Competências  │   └──────────┘
                                            └──────────────┘

