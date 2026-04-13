# Ray-Trace

Um framework de automacao de testes Python/Playwright, pronto para producao, que demonstra padroes corporativos e infraestrutura de testes com qualidade de portfolio.

## Idiomas

- Ingles: [README.md](README.md)
- Portugues (Brasil): este arquivo

## Visao Geral

O **Ray-Trace** e um framework avancado de automacao de testes para a aplicacao [SauceDemo](https://www.saucedemo.com), com foco em:

- **Padroes corporativos**: Page Object Model com hierarquia de componentes
- **Otimizacao de performance**: autenticacao em cache via `storage_state`
- **Observabilidade**: coleta de evidencias em tres camadas (screenshots, videos e traces do Playwright)
- **Resiliencia de rede**: mock de API com cenarios de falha pre-definidos
- **Quality gates visuais**: deteccao de regressao pixel a pixel
- **Integracao CI/CD**: build Docker multi-stage e testes em matriz no GitHub Actions
- **Cenarios reais**: tratamento de flakiness, paridade entre ambientes e publicacao de relatorios

## Stack Tecnologica

- **Testes**: Playwright, pytest, pytest-xdist
- **Linguagem**: Python 3.11+
- **Gerenciamento de dependencias**: Poetry
- **Qualidade de codigo**: Black, Ruff, mypy
- **Relatorios**: Allure, pytest-html
- **Infraestrutura**: Docker, GitHub Actions

## Inicio Rapido

### Setup Local

1. **Clone o repositorio:**
   ```bash
   git clone <repo-url> && cd ray-trace
   ```

2. **Instale o Poetry:**
   ```bash
   pipx install poetry
   ```

3. **Instale as dependencias:**
   ```bash
   poetry install
   ```

4. **Instale os browsers do Playwright:**
   ```bash
   poetry run playwright install chromium
   ```

5. **Configure o ambiente:**
   ```bash
   cp .env.example .env
   ```

6. **Verifique a instalacao:**
   ```bash
   poetry run pytest --collect-only -m smoke
   ```

### Executando os Testes

**Smoke tests (validacao rapida):**
```bash
poetry run pytest -m smoke -v
```

**Regression tests (suite completa):**
```bash
poetry run pytest -m regression -v
```

**Testes de regressao visual:**
```bash
poetry run pytest -m visual -v
```

**Testes de falha de rede/API:**
```bash
poetry run pytest -m network -v
```

**Gerar baselines visuais (primeira execucao):**
```bash
UPDATE_SNAPSHOTS=true poetry run pytest -m visual -v
```

**Rodar arquivo de teste especifico:**
```bash
poetry run pytest tests/e2e/test_auth.py -v
```

**Rodar com browser visivel (debug):**
```bash
HEADLESS=false SLOW_MO_MS=500 poetry run pytest -m smoke -k "test_login"
```

**Rodar em paralelo:**
```bash
poetry run pytest -m regression -n 4 -v
```

### Execucao com Docker

**Build da imagem Docker:**
```bash
docker build -t ray-trace:latest .
```

**Rodar testes no container:**
```bash
docker run --rm \
  -v $(pwd)/test-results:/app/test-results \
  -v $(pwd)/allure-results:/app/allure-results \
  ray-trace:latest \
  -m smoke --alluredir=allure-results
```

**Usando docker-compose:**
```bash
docker-compose up
```

### Geracao de Relatorios

**Gerar relatorio Allure:**
```bash
poetry run pytest -m regression --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

**Visualizar trace do Playwright:**
```bash
poetry run playwright show-trace test-results/{test-name}/trace.zip
```

## Estrutura do Projeto

```text
ray-trace/
├── config/           # Configuracao e dados de teste
│   ├── settings.py   # Settings com Pydantic
│   └── environments.py # Credenciais e dados de produtos
├── pages/            # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_*.py
│   └── components/   # Componentes reutilizaveis
├── fixtures/         # Fixtures de teste
│   ├── auth.py       # Gerenciamento de storage state
│   ├── browsers.py   # Setup de browser/context
│   └── pages.py      # Fixtures de POM
├── utils/            # Utilitarios
│   ├── network_interceptor.py
│   ├── screenshot_comparator.py
│   ├── retry_helper.py
│   └── allure_helpers.py
├── tests/            # Suites de teste
│   ├── e2e/          # Testes end-to-end
│   ├── network/      # Falhas de rede
│   └── visual/       # Regressao visual
├── assets/           # Dados de teste e baselines
│   ├── snapshots/    # Baselines visuais
│   └── test-data/    # Dados JSON/CSV
└── .github/          # Workflows do GitHub Actions
```

## Markers de Teste

- `@pytest.mark.smoke` - suite de validacao rapida
- `@pytest.mark.regression` - suite de regressao completa
- `@pytest.mark.visual` - testes de regressao visual
- `@pytest.mark.network` - cenarios de falha de rede
- `@pytest.mark.critical` - logica critica de negocio
- `@pytest.mark.slow` - testes de longa duracao

## Configuracao

Crie o `.env` a partir do `.env.example`:

```dotenv
APP_ENV=staging
HEADLESS=true
SLOW_MO_MS=0
SNAPSHOT_THRESHOLD=0.02
UPDATE_SNAPSHOTS=false
```

## Autenticacao

Os testes usam autenticacao em cache com `storage_state` do Playwright. Na primeira execucao, o arquivo `.auth/staging_standard_user.json` e criado. Nas execucoes seguintes, esse estado em cache acelera o tempo total de teste.

## Qualidade de Codigo

**Formatar codigo com Black:**
```bash
poetry run black .
```

**Lint com Ruff:**
```bash
poetry run ruff check . --fix
```

**Type check com mypy:**
```bash
poetry run mypy pages/ utils/ config/
```

## Pipeline CI/CD

O GitHub Actions executa um pipeline com multiplos jobs:

1. **Lint e Type Check** - gates de qualidade
2. **Smoke Tests** - validacao rapida
3. **Regression Tests** (matriz) - Chromium, Firefox, WebKit
4. **Visual Tests** - comparacoes de screenshot
5. **Publicacao de relatorios** - Allure no GitHub Pages

## Funcionalidades-Chave

### Page Object Model
- `BasePage` com utilitarios compartilhados
- Cada pagina encapsula interacoes
- Componentes reutilizaveis para UI comum

### Cache de Autenticacao
- Fixture `storage_state` com escopo de sessao
- Elimina login repetitivo por teste
- Acelera a execucao da suite

### Resiliencia de Rede
- `NetworkInterceptor` para injetar falhas de API
- Presets prontos (500, 401, timeout)
- Context manager assincrono para restauracao limpa

### Regressao Visual
- `ScreenshotComparator` para diff pixel a pixel
- Tolerancia configuravel
- Imagens de diff salvas em falha

### Observabilidade
- Screenshot em falha
- Gravacao de video em retry
- Traces do Playwright (somente chromium)
- Integracao com Allure

## Boas Praticas

1. **Evite dados hardcoded** - use `config/environments.py`
2. **Prioridade de localizadores** - `get_by_role` -> `get_by_text` -> seletores CSS
3. **Estrategia de espera** - prefira `wait_for_load_state()` ao inves de `sleep()`
4. **Isolamento dos testes** - nao dependa da ordem de execucao
5. **Assercoes significativas** - valide resultados visiveis para o usuario

## Troubleshooting

**Testes flaky:**
- Aumente timeout: `--timeout=10`
- Adicione waits explicitos: `wait_for_element_visible()`
- Use `@retry` para tentativas no nivel de acao

**Falhas em testes visuais:**
- Atualize baselines: `UPDATE_SNAPSHOTS=true pytest -m visual`
- Revise diffs em `test-results/`
- Ajuste threshold: `SNAPSHOT_THRESHOLD=0.05`

**Problemas com Docker:**
- Rebuild sem cache: `docker build --no-cache -t ray-trace .`
- Verifique browser no container: `docker run ray-trace playwright --version`

## Licenca

MIT

## Autor

DevMiguelPinheiro
