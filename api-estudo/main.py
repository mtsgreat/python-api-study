from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import httpx

app = FastAPI(title="API de Estudo", version="1.0.0")

POKEAPI_BASE = "https://pokeapi.co/api/v2"

class UserCreate(BaseModel):
    """Dados necessários para criar um utilizador."""
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    """Todos os campos são opcionais para permitir updates parciais (PATCH)."""
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class UserResponse(BaseModel):
    """O que a API devolve ao cliente."""
    id: int
    name: str
    email: str
    age: int

# ---------------------------------------------------------------------------
# "Base de dados" em memória (lista simples para estudo)
# ---------------------------------------------------------------------------

db: List[dict] = []
next_id = 1

# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "API de Estudo a funcionar!"}



@app.get("/users", response_model=List[UserResponse])
def list_users():
    return db



@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = next((u for u in db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    return user



@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    global next_id

    # Verifica se o email já existe
    if any(u["email"] == user.email for u in db):
        raise HTTPException(status_code=400, detail="Email já registado")

    new_user = {"id": next_id, **user.model_dump()}
    db.append(new_user)
    next_id += 1

    return new_user



@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate):
    user = next((u for u in db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    
    updates = data.model_dump(exclude_unset=True)
    user.update(updates)

    return user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    global db
    user = next((u for u in db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")

    db = [u for u in db if u["id"] != user_id]



class PokemonStat(BaseModel):
    name: str
    value: int

class PokemonSprites(BaseModel):
    front: Optional[str] = None
    front_shiny: Optional[str] = None

class PokemonResponse(BaseModel):
    id: int
    name: str
    height: float          # em decímetros
    weight: float          # em hectogramas
    base_experience: int
    types: List[str]
    abilities: List[str]
    stats: List[PokemonStat]
    sprites: PokemonSprites

class PokemonListItem(BaseModel):
    name: str
    url: str

class PokemonListResponse(BaseModel):
    count: int
    results: List[PokemonListItem]



@app.get("/pokemon", response_model=PokemonListResponse)
def list_pokemon(limit: int = 20, offset: int = 0):
    with httpx.Client() as client:
        response = client.get(f"{POKEAPI_BASE}/pokemon", params={"limit": limit, "offset": offset})

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Erro ao contactar a PokeAPI")

    data = response.json()
    return PokemonListResponse(count=data["count"], results=data["results"])


@app.get("/pokemon/{name}", response_model=PokemonResponse)
def get_pokemon(name: str):
    with httpx.Client() as client:
        response = client.get(f"{POKEAPI_BASE}/pokemon/{name.lower()}")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"Pokémon '{name}' não encontrado")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Erro ao contactar a PokeAPI")

    data = response.json()

 
    return PokemonResponse(
        id=data["id"],
        name=data["name"],
        height=data["height"],
        weight=data["weight"],
        base_experience=data["base_experience"],
        types=[t["type"]["name"] for t in data["types"]],
        abilities=[a["ability"]["name"] for a in data["abilities"]],
        stats=[PokemonStat(name=s["stat"]["name"], value=s["base_stat"]) for s in data["stats"]],
        sprites=PokemonSprites(
            front=data["sprites"]["front_default"],
            front_shiny=data["sprites"]["front_shiny"],
        ),
    )
