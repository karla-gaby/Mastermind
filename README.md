# Mastermind

Jogo Mastermind desenvolvido com back-end em Python e front-end em Angular 17. Sendo um jogo de dedução, lógica e estratégia.

## Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Back-end | Python 3.11+ · FastAPI · SQLAlchemy |
| Banco de dados | SQLite (sem configuração, arquivo local) |
| Front-end | Angular 17 (componentes standalone) |
| Autenticação | JWT (python-jose + passlib/bcrypt) |


## Pré-requisitos

| Ferramenta | Versão mínima |
|------------|---------------|
| Python | 3.11 |
| Node.js | 20 LTS |
| npm | 9+ |


## Como Rodar

### Back-end

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

O servidor sobe em `http://localhost:8000`.
Documentação interativa disponível em `http://localhost:8000/docs`.

### Front-end

Em outro terminal:

```bash
cd frontend

npm install

npm start
```

A aplicação abre em `http://localhost:4200`.


## Variáveis de Ambiente

Crie o arquivo `backend/.env`:

```env
SECRET_KEY=mastermind-chave-secreta-local-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./mastermind.db
```


## Endpoints da API

### Autenticação

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/registrar` | Cria uma nova conta |
| POST | `/auth/entrar` | Autentica e retorna o token JWT |

### Jogos (requer autenticação)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/jogos/` | Lista o histórico de partidas |
| POST | `/jogos/iniciar` | Inicia uma nova partida |
| GET | `/jogos/{id}` | Retorna o estado de uma partida |
| POST | `/jogos/{id}/tentativa` | Envia uma tentativa |
| POST | `/jogos/{id}/abandonar` | Abandona uma partida ativa |

### Ranking

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/ranking/` | Retorna o ranking global |

---

## Regras do Jogo

- O sistema gera um código secreto com **4 cores** que são sorteadas aleatoriamente
- Cores disponíveis: **Vermelho (R)**, **Verde (G)**, **Azul (B)**, **Amarelo (Y)**, **Laranja (O)**, **Roxo (P)**
- O jogador tem até **10 tentativas** para adivinhar a ordem
- A cada tentativa o sistema retorna:
  - **Exatos** — cores na posição correta
  - **Cores certas** — cores presentes no código mas na posição errada
- O código secreto nunca é enviado ao front-end

### Pontuação

```
Pontuação = (11 - tentativas_usadas) × 100 + max(0, 300 - (duração_segundos ÷ 5))
```

| Tentativa de acerto | Pontos base |
|---------------------|-------------|
| 1ª tentativa | 1000 |
| 5ª tentativa | 600 |
| 10ª tentativa | 100 |
| Não acertou | 0 |

Bônus de velocidade: até **+300 pontos** para partidas rápidas.
Pontuação máxima possível: **1300 pontos**.


## Testes

```bash
cd backend
pytest -v
```

## Estrutura do Projeto

```
Mastermind/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   ├── excecoes.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── game.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   └── game.py
│   │   ├── repositories/
│   │   │   ├── user_repository.py
│   │   │   └── game_repository.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   └── game_service.py
│   │   └── routers/
│   │       ├── auth.py
│   │       ├── games.py
│   │       └── ranking.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_game.py
│   └── requirements.txt
└── frontend/
    └── src/
        ├── app/
        │   ├── app.config.ts
        │   ├── app.routes.ts
        │   ├── guards/
        │   ├── models/
        │   ├── services/
        │   └── components/
        │       ├── login/
        │       ├── navbar/
        │       ├── dashboard/
        │       ├── game/
        │       └── ranking/
        ├── environments/
        └── styles.scss
```

## Banco de Dados

O banco SQLite é criado automaticamente em `backend/mastermind.db` na primeira execução. Nenhuma configuração adicional é necessária.
