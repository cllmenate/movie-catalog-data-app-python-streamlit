# Movie Catalog Data App (Flix App)

Este projeto é uma aplicação web interativa desenvolvida em Python com Streamlit para visualização e gerenciamento de um catálogo de filmes. O sistema atua como um frontend que consome uma API externa para fornecer dados sobre filmes, atores, gêneros e avaliações.

## Sumário
- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação rápida](#instalação-rápida)
- [Configuração](#configuração)
- [Uso / Exemplos](#uso--exemplos)
- [Dados e contratos](#dados-e-contratos)
- [Testes](#testes)
- [CI / CD](#ci-cd)
- [Deploy](#deploy)
- [Observabilidade e alertas](#observabilidade-e-alertas)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Autores / Contato](#autores--contato)
- [ChangeLog](#changelog)

## Sobre o projeto
O Flix App é um sistema de recomendação e catálogo de filmes. O objetivo principal é fornecer uma interface amigável para explorar dados cinematográficos, visualizar estatísticas e gerenciar registros através de uma API RESTful.

O projeto está configurado como um pacote Python moderno, utilizando pyproject.toml para gerenciamento de dependências e metadados.

## Funcionalidades
O aplicativo conta com um sistema de autenticação e um menu lateral de navegação com as seguintes seções:
* **Home:** Tela de boas-vindas e introdução ao sistema.
* **Login:** Sistema de autenticação via token para acesso aos recursos protegidos.
* **Stats:** Dashboard com estatísticas sobre o catálogo (provavelmente visualizações com Plotly).
* **Actors:** Consulta e gerenciamento de atores.
* **Genres:** Consulta e gerenciamento de gêneros de filmes.
* **Movies:** Catálogo principal de filmes.
* **Reviews:** Gestão e visualização de avaliações de usuários.
* **About / Contact:** Informações institucionais do projeto.

## Arquitetura
O projeto segue uma arquitetura modular organizada por domínios funcionais (Feature-based folder structure). Cada entidade do sistema (Atores, Filmes, Gêneros, etc.) possui seu próprio diretório contendo camadas de responsabilidade:
* **Page (page.py):** Responsável pela interface do usuário (UI) usando Streamlit.
* **Service (service.py):** Camada de lógica de negócios e comunicação com a API.
* **Repository (repository.py):** Abstração para manipulação de dados.

**Tecnologias principais:**
* **Linguagem:** Python >= 3.13
* **Frontend:** Streamlit
* **Visualização de Dados:** Plotly e Streamlit-AgGrid
* **Manipulação de Dados:** Pandas
* **HTTP Client:** Requests

## Pré-requisitos
* **Python:** `>=3.13`
* **Gerenciador de pacotes:** `pip` ou `uv` (recomendado, visto o arquivo `uv.lock`).

**Dependências principais:**
* `pandas` (Manipulação de dados)
* `scikit-learn` (Modelagem e métricas)
* `joblib` (Serialização de objetos)
* `ipykernel` (Execução do notebook)

## Instalação rápida

1.  Clone este repositório:
    ```bash
    git clone https://github.com/cllmenate/movie-catalog-data-app-python-streamlit.git
    cd movie-catalog-data-app-python-streamlit
    ```

2.  Instale as dependências. Se estiver usando `pip`:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # ou
    .venv\Scripts\activate     # Windows
    ```

    ```bash
    pip install -r requirements.txt
    ```

    *Dica: Se estiver usando `uv`, basta rodar `uv sync`.*

## Configuração
A estrutura de pastas esperada pelo projeto é a seguinte:

```text
.
├── actors/
│   └── page.py      # Página de atores
│   └── service.py   # Serviço de atores
│   └── repository.py   # Repositório de atores
├── api/
│   └── service.py   # Serviço de API
├── genres/
│   └── page.py      # Página de gêneros
│   └── service.py   # Serviço de gêneros
│   └── repository.py   # Repositório de gêneros
├── login/
│   └── page.py      # Página de login
│   └── service.py   # Serviço de login
│   └── repository.py   # Repositório de login
├── movies  /
│   └── page.py      # Página de filmes
│   └── service.py   # Serviço de filmes
│   └── repository.py   # Repositório de filmes
├── reviews/
│   └── page.py      # Página de avaliações
│   └── service.py   # Serviço de avaliações
│   └── repository.py   # Repositório de avaliações
├── stats/
│   └── page.py      # Página de estatísticas
│   └── service.py   # Serviço de estatísticas
│   └── repository.py   # Repositório de estatísticas
├── tests/
│   └── conftest.py      # Configuração de testes
│   └── test_genres_repository.py   # Testes de gêneros
│   └── test_genres_service.py   # Testes de gêneros
│   └── test_movies_repository.py   # Testes de filmes
│   └── test_movies_service.py   # Testes de filmes
├── main.py          # Ponto de entrada da aplicação
└── config.toml   # Configuração do projeto
└── pyproject.toml              # Definição do projeto e dependências
└── .gitignore
└── LICENSE
└── .python-version
└── README.md
└── uv.lock
```

## Uso / Exemplos
Para iniciar a aplicação, execute o comando na raiz do projeto:

```bash
streamlit run main.py
```

Ao abrir o navegador:
1. Você será redirecionado para a tela de Login.
2. Insira suas credenciais. O sistema tentará autenticar na API externa.
3. Após o sucesso, o token será salvo no st.session_state e o menu lateral ficará disponível.

## Dados e contratos
A aplicação consome dados de uma API externa.
* **Base URL:** `https://callmenate.pythonanywhere.com/api/v1/`
* **Autenticação:** Endpoint `/authentication/token/` (POST) recebendo username e password.

Os dados retornados (JSON) são processados via `pandas` para exibição em tabelas e gráficos.

## Testes
O projeto utiliza pytest para testes automatizados. A estrutura de testes reflete a organização dos módulos (ex: test_genres_repository.py, test_movies_service.py).

Para executar os testes:
```bash
pytest
```
Para verificar a conformidade do código (linter), o projeto utiliza o ruff:
```bash
ruff check .
```

## CI / CD
(Seção sugerida para implementação futura, baseada nas ferramentas instaladas) O projeto está preparado para pipelines de Integração Contínua que executem:
1. Instalação de dependências.
2. Linting com ruff.
3. Testes unitários com pytest.

## Deploy
A aplicação é compatível com Streamlit Cloud.
1. Conecte seu repositório ao Streamlit Cloud.
2. Aponte o arquivo principal para main.py.
3. Certifique-se de selecionar a versão correta do Python (3.13+).

## Observabilidade e alertas
Atualmente, o feedback de erros de conexão é exibido diretamente na interface do usuário (ex: falha de login retorna status code e mensagem de erro).

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* ou enviar *pull requests*.

1.  Faça um Fork do projeto.
2.  Crie uma Branch para sua Feature (`git checkout -b feature/MinhaFeature`).
3.  Faça o Commit de suas mudanças (`git commit -m 'Adicionando nova feature'`).
4.  Faça o Push para a Branch (`git push origin feature/MinhaFeature`).
5.  Abra um Pull Request.

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autores / Contato
Desenvolvido como parte de um portfólio de Data App.
* **Nattam Pereira** - *Trabalho inicial* - Copyright (c) 2026

## ChangeLog
* 0.1.0 - Versão inicial com catálogo de filmes, atores, gêneros e autenticação.
