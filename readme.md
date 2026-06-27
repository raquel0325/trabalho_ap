Projeto - Conectar-CE

O **Conectar-CE** é uma plataforma digital centralizada focada em fortalecer o mercado de trabalho na região do Crajubar (Crato, Juazeiro do Norte e Barbalha). O sistema atua como um hub de empregabilidade, digitalizando o "boca a boca" regional e conectando contratantes a trabalhadores 
de forma rápida e gratuita.

## 🚀 Funcionalidades (MVP)
- Cadastro e Login (inclui autenticação local e Google OAuth).
- Mural de vagas com filtros por cidade (Juazeiro, Crato, Barbalha) e busca.
- Perfil profissional para candidatos (questionário + competências).
- Match automático: recomenda vagas compatíveis com base nas competências.
- Candidatura a vagas com verificação de duplicidade e histórico.
- Área de empresas/contratantes para criar e gerenciar vagas.

## 📝 Tecnologias Utilizadas
- **Painel do funcionário :** seção de perfil com modo visualização/edição, gerenciamento de competências e **recomendações** 
- **Freelance (novo módulo):** cadastrar/editar/excluir freelances, ver **solicitantes** e acompanhar **contratações**.
- **Avaliação de freelancers:** empresas podem avaliar freelancers após contratação (nota + comentário).
- **Notificações e vagas salvas:** exibição na lateral direita (accordion) com listagem e ações.
- **Painel da empresa:** abas (Perfil, Dashboard, Vagas), com estatísticas e ações rápidas (criar vagas) + seções de contratados e notificações.

## Visão Geral

O Conectar-CE é uma aplicação web desenvolvida em Flask que permite:
    **Funcionários:** cadastrar-se, preencher perfil profissional com competências, buscar vagas compatíveis e candidatar-se.
    **Empresas:** cadastrar-se e publicar vagas com requisitos de competências.
    **Sistema de Match:** calcula automaticamente a compatibilidade entre o perfil do candidato e os requisitos da vaga.

## Funcionalidades
**Para Funcionários:**
    * Cadastro* com autenticação local ou Google OAuth.
    Questionário complementar com dados profissionais.
    * Seleção* e adição de competências personalizadas (inclui adicionar competências novas).
    Listagem de vagas com filtros (busca, salário, empresa).
    * Visualização* de vagas recomendadas por compatibilidade.
    Candidatura a vagas com verificação de duplicidade.
    * Histórico* de candidaturas.

**Para Empresas:**
    Criação de vagas com competências necessárias.
    Gestão de vagas publicadas e candidaturas.
    Gestão do módulo **Freelance** (contratações e avaliações).


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

conectar-ce/
│
├── app.py                              # Inicializa a aplicação Flask
├── config.py                           # Variáveis de ambiente/configurações
├── database/                          # Banco e inicialização
│   ├── connect.py                     # Conexão SQLite (get_connection)
│   └── main.py                        # init_db(): cria/atualiza tabelas
│
├── CRUDs/                              # Camada de acesso ao banco (CRUD)
│   ├── candidatura.py                # Candidaturas + match (quando aplicável)
│   ├── crud_contratar.py             # Contratações (freelance)
│   ├── crud_freelancer.py            # Freelancers
│   ├── crud_comp.py                 # Competências
│   ├── crud_func.py                 # Funcionários
│   ├── crud_emp.py                  # Empresas
│   ├── crud_quest.py                # Questionário/respostas
│   ├── crud_notificacao.py          # Notificações
│   └── crud_vagas.py               # Vagas + vínculo com competências
│
├── models/                             # Regras de negócio (camada de domínio)
│   ├── model_fun.py                   # Funcionário
│   ├── model_emp.py                   # Empresa
│   ├── model_comp.py                  # Competência
│   ├── model_quest.py                 # Questionário
│   ├── model_vagas.py                 # Vaga/Candidatura/Match
│   ├── model_freelancer.py           # Freelancer
│   ├── model_contratar.py            # Contratação
│   └── model_notificacao.py          # Notificação
│
├── routes/                             # Rotas HTTP (controllers)
│   ├── auth.py                         # Login/cadastro (base)
│   ├── google_auth.py                 # OAuth Google
│   ├── home.py                         # /home e /logout + dashboard
│   ├── questionario.py               # /questionario e salvar
│   ├── vagas.py                       # /vagas, detalhes e candidatura
│   └── freelancer.py                 # rotas do módulo freelance (criar/editar/excluir/fluxos)
│
├── static/
│   ├── css/                          # estilos
│   └── script/                       # JS da interface (home_func.js, home_emp.js etc.)
│
└── templates/                         # Templates Jinja2
    ├── index.html                     # Login/cadastro
    ├── home/home_func.html          # Dashboard funcionário
    ├── home/home_emp.html           # Dashboard empresa
    ├── questionario.html            # Questionário
    └── vaga/                        # Área de vagas (listagem/detalhe/candidaturas)
        ├── vagas_listar.html
        ├── vagas_recomendadas.html
        ├── vaga_detalhe.html
        └── candidaturas.html


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

**FREELANCERS / FREELANCE==========================**
*Coluna	      | Tipo	 | Descrição*
id_freelancer |INTEGER  |PK Identificador único
id_funcionario|INTEGER |FK Funcionário (dono do freelance)
profissao	 |TEXT	     |Profissão/título do anúncio
servico_oferecido|TEXT  |Descrição do serviço
preco_medio	|REAL	     |Preço médio cobrado
disponibilidade|TEXT |Disponível/ocupado/indisponível

**CONTRATACOES====================================**
*Coluna	      | Tipo	 | Descrição*
id_contratacao|INTEGER  |PK Identificador único
id_freelancer  |INTEGER  |FK Freelance
id_contratante |INTEGER  |FK Empresa ou funcionário
tipo_contratante|TEXT    |empresa/funcionario
data_contratacao|TIMESTAMP|Data do pedido
status	    |TEXT	     |pendente/aceito/recusado/concluido/cancelado
data_conclusao|TIMESTAMP|Data quando concluído

**AVALIACOES======================================**
*Coluna	      | Tipo	 | Descrição*
id_avaliacao  |INTEGER  |PK Identificador único
id_freelancer |INTEGER  |FK Freelance
id_contratante|INTEGER  |FK Contratante
tipo_contratante|TEXT   |
ota	        |INTEGER |1..5
comentario	|TEXT	     |Comentário do contratante
data_avaliacao|TIMESTAMP|Data da avaliação

**NOTIFICACOES====================================**
*Coluna	      | Tipo	 | Descrição*
id_notificacao|INTEGER  |PK Identificador único
id_usuario	 |INTEGER  |Usuário que recebe
titulo	    |TEXT	     |
mensagem	  |TEXT	     |
tipo	      |TEXT	     |
id_referencia|INTEGER  |Relaciona com contrato/solicitação etc.
lida	       |INTEGER  |0/1
data_criacao|TIMESTAMP|Data de criação


## Rotas da Aplicação ==============================================================================

*Autenticação (routes/auth.py)*
Rotas                 | Descrição
--------------------- | -------------
/                     | Página inicial (antes do login)
/login                | Login autenticação
/cadastro/funcionario | Cadastro de funcionário
/cadastro/empresa     | Cadastro de empresa

*Google Auth (routes/google_auth.py)*
Rotas                 | Descrição
--------------------- | -------------
/google-login         | Login com Google
/signin-google        | Redirecionamento após OAuth

*Home (routes/home.py)*
Rotas                 | Descrição
--------------------- | -------------
/home                 | Dashboard (funcionário ou empresa)
/logout               | Logout

*Questionário (routes/questionario.py)*
Rotas                  | Descrição
---------------------  | -------------
/questionario/<id_func>| Página do questionário
/salvar_questionario   | Salva questionário e competências

*Candidatar / Vagas (routes/candidatar_se.py)*
Rotas                       | Descrição
---------------------------| -------------
/vaga/<id_vaga>            | Detalhes da vaga
/vaga/<id_vaga>/candidatar| Candidatar-se à vaga
/cancelar_candidatura/<id_candidatura> | Cancelar candidatura
/candidatura/<id_candidatura>/status | Alterar status da candidatura (empresa)
/vaga/<id_vaga>/candidatos | Listar candidatos (empresa)

*Vagas & Gestão (routes/route_vagas.py)*
Rotas                       | Descrição
---------------------------| -------------
/vagas                      | Listagem de vagas com filtros
/empresa/vaga/criar         | Criar vaga (empresa)
/empresa/vagas              | Vagas da empresa (dashboard)
/vaga/excluir/<id_vaga>    | Excluir vaga (empresa)
/vaga/<id_vaga>/editar      | Editar vaga (empresa)

*Atualização de Perfil (routes/atualizar_perfil.py)*
Rotas                       | Descrição
---------------------------| -------------
/atualizar_perfil          | Atualizar dados + questionário (funcionário)
/atualizar_competencias    | Atualizar competências do funcionário
/atualizar_empresa         | Atualizar perfil da empresa

*Avaliações (routes/route_avaliacao.py)*
Rotas                         | Descrição
----------------------------| -------------
/avaliar/<id_freelancer>    | Enviar avaliação (empresa)
/avaliacoes/<id_freelancer> | Ver avaliações de um freelancer

*Freelance (routes/route_freelancer.py)*
Rotas (principais)          | Descrição
-----------------------------| -------------
/freelancer                  | Buscar freelancers (filtros)
/freelancer/cadastrar       | Cadastrar freelance (funcionário)
/freelancer/editar/<id>    | Editar freelance (funcionário)
/freelancer/excluir/<id>   | Excluir freelance (DELETE)

*Contratar & Solicitantes (routes/route_contratarfreelas.py e routes/route_solicitante.py)*
Rotas (principais)          | Descrição
-----------------------------| -------------
/contratar/<id_freelancer> | Contratar freelancer (cria contratação e notifica)
/freelancer/<id_freelancer>/solicitantes | Ver solicitantes do freelancer
/contratacao/<id_contratacao>/status | Atualizar status da contratação (funcionário dono)


## Modelos e Regras de Negócio =====================================================================
Arquitetura em 3 Camadas
Routes (rotas) → Models (regras) → CRUDs (banco)

*Validações Principais*

- **Funcionário:**
  - Nome mínimo 3 caracteres.
  - E-mail deve conter `@`.
  - Senha mínima 6 caracteres.
  - CPF exatamente 11 dígitos.
- **Empresa:**
  - Nome mínimo 2 caracteres.
  - CNPJ exatamente 14 dígitos.
  - E-mail deve conter `@`.
  - Senha mínima 6 caracteres.
- **Vaga:**
  - Descrição mínima 50 caracteres.
  - Salário não pode ser negativo.
  - Pelo menos uma competência necessária.
- **Candidatura:**
  - Um funcionário não pode se candidatar duas vezes à mesma vaga.
  - Status de candidatura deve ser válido.
- **Freelance / Contratação:**
  - Contratar freelancer cria contratação no estado inicial (pendente).
  - Atualização de status só aceita valores válidos: pendente/aceito/recusado/concluido/cancelado.
  - Avaliação só pode ser feita após contratação válida e garante que o contratante é quem realmente contratou.

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
    *Login/Cadastro (index.html)*                 - Página inicial com formulários de acesso
    *Home Funcionário (home/home_func.html)*    - Dashboard do funcionário (perfil, competências, recomendações, freelances, contratados, notificações, vagas salvas)
    *Home Empresa (home/home_emp.html)*         - Dashboard da empresa (perfil, estatísticas, vagas, contratados e notificações)
    *Questionário (questionario.html)*         - Formulário de perfil profissional (dados + competências)
    *Lista de Vagas (vagas_listar.html)*        - Vagas com filtros e match
    *Detalhe da Vaga (vaga_detalhe.html)*       - Informações completas e ações de candidatura
    *Candidaturas (candidaturas.html)*        - Histórico/lista de candidaturas do funcionário
    *Freelancer Listar (freelancer_listar.html)*- Lista/busca de freelancers (com status de contratação e avaliações)
    *Editar Freelancer (editar_freelance.html)*- Edição de um freelance do funcionário
    *Ver Solicitantes (ver_solicitantes.html)* - Lista de solicitantes de um freelancer
    *Criar Vaga (criar_vaga.html)*              - Formulário para criação de novas vagas (empresa)
    *Editar Vaga (editar_vaga.html)*            - Edição de uma vaga existente (empresa)
    *Avaliações (ver-avaliacao.html)*          - Página para ver avaliações de um freelancer

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

