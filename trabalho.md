# Apresentação do Projeto — Conectar-CE

## 1) Título do Projeto
**Conectar-CE — Plataforma de Empregabilidade para a Região do Crajubar (Crato, Juazeiro do Norte e Barbalha)**

## 2) Integrantes da Equipe (modelo)
- **[Nome 1] — Função 1 (ex.: Backend / Rotas / Models)**
- **[Nome 2] — Função 2 (ex.: Frontend / Templates / CSS/JS)**
- **[Nome 3] — Função 3 (ex.: Banco de dados / CRUDs / Modelagem)**
- **[Nome 4] — Função 4 (ex.: Integração / Testes / Documentação)**

> Substituir os campos entre colchetes pelos nomes e funções reais.

## 3) Demonstração Prática (o que será mostrado)
Nesta apresentação, mostramos o funcionamento do **Conectar-CE** como um hub de empregabilidade, conectando **funcionários (candidatos)** e **empresas (contratantes)**.

### Fluxo do Funcionário
1. **Cadastro e Login:** o usuário entra no sistema (com autenticação local e possibilidade de Google OAuth, quando aplicável).
2. **Questionário e Competências:** após o cadastro, o candidato preenche dados do perfil e seleciona suas competências.
3. **Recomendações e Match automático:** no dashboard, o sistema exibe **vagas recomendadas**, incluindo um indicador de compatibilidade (match) baseado nas competências.
4. **Detalhe da vaga e candidatura:** ao acessar uma vaga, o usuário pode **se candidatar**, e o sistema registra o histórico e evita duplicidade (o mesmo candidato não se candidata duas vezes à mesma vaga).

### Módulo Freelance (funcionário)
5. **Publicação de Freelances:** o funcionário pode anunciar seus serviços, com informações como profissão, descrição, preço médio e disponibilidade.
6. **Solicitantes e Contratações:** ao longo do processo, o usuário acompanha solicitantes e contratações relacionadas ao seu anúncio.
7. **Avaliações:** após a contratação, o sistema permite avaliações (nota e comentário), garantindo rastreabilidade do processo.

### Fluxo da Empresa
8. **Painel da Empresa:** a empresa cria e gerencia vagas, visualiza candidatos/contratações e mantém o controle das informações.

## 4) Código Relevante (3 trechos para explicar)
> Observação importante: como o arquivo solicitado para preenchimento é o `trabalho.md` (texto da apresentação), este bloco foi deixado como “modelo” para você inserir os **trechos reais** do seu projeto. Assim, você garante que o trecho citado é exatamente o que está no seu código.

### Trecho 1 — Cálculo do Match (competências → compatibilidade)
- **O que faz:** calcula o percentual de compatibilidade entre as **competências do funcionário** e as **competências exigidas pela vaga**.
- **Por que é relevante:** esse trecho representa o diferencial do Conectar-CE, pois transforma perfil e requisitos em uma recomendação objetiva.

**Inserir aqui o trecho real do código:**
```python
# cole o trecho real (função/algoritmo do match)
```

### Trecho 2 — Validação de duplicidade na candidatura
- **O que faz:** antes de salvar a candidatura, valida se o funcionário **já se candidatou** àquela vaga, impedindo duplicidade.
- **Por que é relevante:** garante consistência dos dados e melhora a confiabilidade do histórico de candidaturas.

**Inserir aqui o trecho real do código:**
```python
# cole o trecho real (validação/consulta antes de inserir candidatura)
```

### Trecho 3 — Atualização de status de candidatura/contratação
- **O que faz:** controla alterações de status, garantindo que a aplicação trabalhe com valores válidos (ex.: pendente/aceito/recusado/concluido/cancelado) e que cada mudança seja registrada.
- **Por que é relevante:** mostra que o sistema possui regras de negócio e fluxo operacional completo.

**Inserir aqui o trecho real do código:**
```python
# cole o trecho real (endpoint/validação do status)
```

## 5) Ferramentas Utilizadas
- **Python 3.x**
- **Flask** (framework web)
- **SQLite3** (banco de dados)
- **Authlib** (autenticação OAuth Google)
- **HTML5/CSS3** (interface)
- **JavaScript** (interatividade front-end)
- **Jinja2** (templates)

## 6) Desafios e Aprendizados
### Principais desafios
- Implementar o **match automático** com base nas competências, garantindo que o resultado faça sentido para o usuário.
- Manter **consistência** no banco de dados e nas regras (por exemplo, impedir duplicidade de candidatura e manter histórico confiável).
- Organizar a aplicação com separação clara entre **rotas (views), models (regras)** e **CRUDs (acesso ao banco)**.
- Integrar telas e fluxos (funcionário e empresa) de forma que a experiência do usuário fosse simples.

### Aprendizados
- Estruturação de projeto com melhor organização em camadas.
- Implementação de regras de negócio aplicadas diretamente no fluxo do sistema.
- Desenvolvimento de uma interface funcional e coerente, conectando perfil, competências, recomendações e ações do usuário.

### Possibilidades de expansão / melhorias futuras
- Refinar o algoritmo de recomendação (match) com critérios adicionais.
- Melhorar filtros por cidade, salário e outras preferências.
- Ampliar o módulo de freelances com etapas mais detalhadas e automações.

## 7) Fechamento (frase final)
Concluímos que o Conectar-CE facilita a conexão entre candidatos e empresas ao integrar **perfil**, **competências**, **match automático** e **fluxos de candidatura/contratação**, oferecendo uma solução mais organizada e rápida para a região do Crajubar.

