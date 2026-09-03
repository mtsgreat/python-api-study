# API de Estudo — FastAPI + Pydantic

Projecto de estudo para aprender a construir APIs REST com Python, usando **FastAPI** e **Pydantic**. Inclui um CRUD simples de utilizadores e integração com a [PokeAPI](https://pokeapi.co) para demonstrar como consumir uma API externa e estruturar os dados de retorno.

---

## Tecnologias

| Ferramenta | Versão | Função |
|---|---|---|
| Python | 3.12 | linguagem |
| FastAPI | 0.115.0 | framework web |
| Pydantic | 2.9.2 | validação e tipagem dos dados |
| Uvicorn | 0.30.6 | servidor ASGI (equivalente ao Node HTTP) |
| httpx | 0.27.2 | cliente HTTP para chamar APIs externas |

---

## Conceitos abordados

### FastAPI
Framework moderno e de alto desempenho para construir APIs com Python. Gera automaticamente documentação interativa (Swagger UI) em `/docs` sem configuração adicional.

### Pydantic
Biblioteca de validação de dados equivalente ao **Zod** no TypeScript. Define a estrutura esperada dos dados usando classes Python com type hints. Valida automaticamente os tipos, converte valores quando possível e devolve erros claros quando os dados são inválidos.

```python
# Pydantic (Python)          vs         Zod (TypeScript)
class User(BaseModel):                # const UserSchema = z.object({
    name: str                         #   name: z.string(),
    age: int                          #   age: z.number(),
                                      # })
```

### httpx
Cliente HTTP para Python usado para fazer requests a APIs externas de forma síncrona ou assíncrona.

---

## Instalação

```bash
# 1. Clonar o repositório
git clone <url-do-repo>
cd api-estudo

# 2. Criar ambiente virtual
python -m venv venv

# 3. Activar o ambiente virtual
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt
```

---

## Arrancar o servidor

```bash
.\venv\Scripts\uvicorn.exe main:app --reload
```

O servidor fica disponível em `http://localhost:8000`.  
A documentação interativa fica em `http://localhost:8000/docs`.

---

## Endpoints

### Utilizadores (CRUD em memória)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/users` | listar todos os utilizadores |
| `GET` | `/users/{id}` | buscar utilizador por id |
| `POST` | `/users` | criar utilizador |
| `PATCH` | `/users/{id}` | actualizar campos de um utilizador |
| `DELETE` | `/users/{id}` | apagar utilizador |

**Criar utilizador — exemplo de body:**
```json
{
  "name": "Mateus",
  "email": "mateus@email.com",
  "age": 25
}
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Mateus",
  "email": "mateus@email.com",
  "age": 25
}
```

---

### Pokémon (integração com PokeAPI)

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/pokemon?limit=20&offset=0` | listar pokémons com paginação |
| `GET` | `/pokemon/{name}` | detalhes de um pokémon pelo nome ou id |

A PokeAPI devolve um JSON com mais de 200 campos por Pokémon. O Pydantic filtra e estrutura apenas os dados relevantes.

**Exemplo — `GET /pokemon/pikachu`:**
```json
{
  "id": 25,
  "name": "pikachu",
  "height": 4,
  "weight": 60,
  "base_experience": 112,
  "types": ["electric"],
  "abilities": ["static", "lightning-rod"],
  "stats": [
    { "name": "hp", "value": 35 },
    { "name": "attack", "value": 55 },
    { "name": "defense", "value": 40 },
    { "name": "special-attack", "value": 50 },
    { "name": "special-defense", "value": 50 },
    { "name": "speed", "value": 90 }
  ],
  "sprites": {
    "front": "https://raw.githubusercontent.com/.../pikachu.png",
    "front_shiny": "https://raw.githubusercontent.com/.../pikachu_shiny.png"
  }
}
```

---

## Estrutura do projecto

```
api-estudo/
├── venv/               # ambiente virtual (não commitar)
├── main.py             # código da API
├── requirements.txt    # dependências
└── README.md
```

---

## Notas

- Os dados dos utilizadores são guardados **em memória** — reiniciar o servidor apaga tudo. Num projecto real usaria-se uma base de dados (PostgreSQL, SQLite, etc.).
- O Python 3.14 ainda não é suportado pelo Pydantic v2 (falta de wheels pré-compiladas para o `pydantic-core`). Usar **Python 3.12**.
