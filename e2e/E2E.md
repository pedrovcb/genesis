# E2E Tests — ARCA Gênesis

Testes end-to-end usando **Selenium + Python + pytest** para a plataforma Genesis.

## Setup

### 1. Instalar dependências

```bash
cd e2e
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

No arquivo `../.env`, adicione:

```env
E2E_BASE_URL=http://localhost:3000
E2E_API_URL=http://localhost:8000/api
E2E_TEST_EMAIL=teste_e2e@genesis.com
E2E_TEST_PASSWORD=senha_teste_123
```

> User de teste é criado automaticamente na primeira rodada. Se já existir, é reutilizado.

### 3. Iniciar serviços

```bash
# Na raiz do projeto
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Aguarde serviços ficarem disponíveis:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Rodar testes

### Todos os testes

```bash
pytest tests/ -v
```

### Teste específico

```bash
pytest tests/test_auth.py::TestAuth::test_login_valido -v
```

### Com relatório HTML

```bash
pytest tests/ -v --html=report.html --self-contained-html
```

### Modo verbose + live logs

```bash
pytest tests/ -vv -s
```

## Estrutura

```
e2e/
├── conftest.py             # Fixtures do Selenium
├── pages/                  # Page Object Model
│   ├── login_page.py       # Tela de login
│   ├── cadastro_page.py    # Tela de cadastro
│   ├── home_page.py        # Tela Home
│   ├── emergencia_page.py  # Modo Emergência
│   └── protocolo_page.py   # Página protocolo/fluxograma
├── tests/
│   ├── test_auth.py        # 6 testes: login + cadastro
│   ├── test_home.py        # 3 testes: home + busca
│   ├── test_emergencia.py  # 4 testes: emergência + favoritos
│   └── test_protocolo.py   # 4 testes: fluxograma
└── requirements.txt        # Dependências Python
```

## Seletores

Os testes usam seletores CSS baseados em:

- Placeholder text: `input[placeholder="Email"]`
- Classes existentes: `.login-btn-entrar`, `.protocol-card`, `.back-btn`
- Aria labels: `button[aria-label="Home"]`
- Text content (XPath): testes que buscam por texto em buttons

## Cenários Cobertos

### Autenticação (test_auth.py)
1. Login com credenciais válidas → Home
2. Login com senha errada → erro visível
3. Login com campos vazios → não navega
4. Cadastro bem-sucedido → volta a login
5. Cadastro com senhas diferentes → erro
6. Voltar do cadastro → retorna a login

### Home (test_home.py)
7. Home exibe corretamente após login
8. Buscar protocolo ("dengue") → resultado no dropdown
9. Botão Modo Emergência está ativo e clicável

### Modo Emergência (test_emergencia.py)
10. Modo Emergência carrega com lista de protocolos
11. Favoritar protocolo (toggle estrela)
12. Selecionar protocolo → navega para protocolo
13. Timer rodando (se desktop)

### Protocolo (test_protocolo.py)
14. Protocolo exibe título e nós do fluxograma
15. Expandir nó → mostra filhos
16. Back button → volta para Emergência
17. Favoritar dentro do protocolo → toggle

## Notas

- **Chrome headless**: Testes rodam sem interface gráfica (mais rápido)
- **Timeout padrão**: 10 segundos por elemento
- **DB externo**: Testes usam a base Neon PostgreSQL real
- **Cleanup**: Cada teste limpa localStorage e cookies antes de rodar

## Troubleshooting

### Chrome não encontrado
```bash
# webdriver-manager baixa automaticamente, mas se houver problema:
export CHROMEDRIVER_PATH=/usr/bin/chromedriver
```

### Timeout esperando elemento
- Aumentar `implicitly_wait` em `conftest.py`
- Verificar se URL do app está correta em `.env`

### Elemento não encontrado
- Inspecionar elemento no browser
- Verificar se seletor CSS está correto
- Considerar adicionar `data-testid` ao código

## Suporte

Verifique:
1. Se serviços estão rodando: `docker ps`
2. Se frontend carrega: http://localhost:3000
3. Se logs têm erros: `pytest tests/ -vv -s`
