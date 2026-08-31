from datetime import datetime, timezone
from typing import Dict, List
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

# Inicialização da Aplicação
app = FastAPI(title="API de Estatísticas de Jogadores", version="1.0")

# Modelos de Dados (Pydantic)
class JogadorEntrada(BaseModel):
    nickname: str = Field(min_length=3, max_length=30)
    plataforma: str = Field(min_length=2, max_length=20)
    rank: str = Field(default="Unranked", max_length=20)

class Jogador(JogadorEntrada):
    id: int

class PartidaEntrada(BaseModel):
    gols: int = Field(ge=0)
    assistencias: int = Field(ge=0)
    defesas: int = Field(ge=0)
    resultado: str = Field(pattern="^(vitoria|derrota|empate)$")

class Partida(PartidaEntrada):
    id: int
    jogador_id: int
    instante: str

# Camada de Persistência e Repositório (Em Memória)
class Database:
    def __init__(self):
        self.jogadores: Dict[int, Jogador] = {}
        self.partidas: Dict[int, Partida] = {}
        self._id_jogador = 0
        self._id_partida = 0
        self._seed()

    def _next_id_jogador(self) -> int:
        self._id_jogador += 1
        return self._id_jogador

    def _next_id_partida(self) -> int:
        self._id_partida += 1
        return self._id_partida

    def _seed(self):
        j1 = self.salvar_jogador(JogadorEntrada(nickname="Fennec", plataforma="PC", rank="Grand Champion"))
        j2 = self.salvar_jogador(JogadorEntrada(nickname="Breakout", plataforma="PlayStation", rank="Gold"))
        
        self.salvar_partida(j1.id, PartidaEntrada(gols=3, assistencias=2, defesas=1, resultado="vitoria"))
        self.salvar_partida(j1.id, PartidaEntrada(gols=1, assistencias=0, defesas=4, resultado="derrota"))

    def validar_nickname_unico(self, nickname: str, ignorar_id: int = None):
        for j in self.jogadores.values():
            if j.id != ignorar_id and j.nickname.lower() == nickname.lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"O nickname '{nickname}' já está em uso."
                )

    def obter_jogador_ou_404(self, jogador_id: int) -> Jogador:
        if jogador_id not in self.jogadores:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jogador não encontrado")
        return self.jogadores[jogador_id]

    def salvar_jogador(self, entrada: JogadorEntrada) -> Jogador:
        self.validar_nickname_unico(entrada.nickname)
        novo_id = self._next_id_jogador()
        jogador = Jogador(id=novo_id, **entrada.model_dump())
        self.jogadores[novo_id] = jogador
        return jogador

    def atualizar_jogador(self, jogador_id: int, entrada: JogadorEntrada) -> Jogador:
        self.obter_jogador_ou_404(jogador_id)
        self.validar_nickname_unico(entrada.nickname, ignorar_id=jogador_id)
        jogador = Jogador(id=jogador_id, **entrada.model_dump())
        self.jogadores[jogador_id] = jogador
        return jogador

    def remover_jogador(self, jogador_id: int):
        self.obter_jogador_ou_404(jogador_id)
        del self.jogadores[jogador_id]
        self.partidas = {p_id: p for p_id, p in self.partidas.items() if p.jogador_id != jogador_id}

    def salvar_partida(self, jogador_id: int, entrada: PartidaEntrada) -> Partida:
        self.obter_jogador_ou_404(jogador_id)
        novo_id = self._next_id_partida()
        partida = Partida(
            id=novo_id,
            jogador_id=jogador_id,
            instante=datetime.now(timezone.utc).isoformat(),
            **entrada.model_dump()
        )
        self.partidas[novo_id] = partida
        return partida

    def listar_partidas_jogador(self, jogador_id: int) -> List[Partida]:
        self.obter_jogador_ou_404(jogador_id)
        return [p for p in self.partidas.values() if p.jogador_id == jogador_id]

db = Database()

# Endpoints - Jogadores
@app.get("/jogadores", response_model=List[Jogador])
def listar_jogadores():
    return list(db.jogadores.values())

@app.get("/jogadores/{jogador_id}", response_model=Jogador)
def obter_jogador(jogador_id: int):
    return db.obter_jogador_ou_404(jogador_id)

@app.post("/jogadores", response_model=Jogador, status_code=status.HTTP_201_CREATED)
def criar_jogador(entrada: JogadorEntrada, response: Response):
    jogador = db.salvar_jogador(entrada)
    response.headers["Location"] = f"/jogadores/{jogador.id}"
    return jogador

@app.put("/jogadores/{jogador_id}", response_model=Jogador)
def atualizar_jogador(jogador_id: int, entrada: JogadorEntrada):
    return db.atualizar_jogador(jogador_id, entrada)

@app.delete("/jogadores/{jogador_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_jogador(jogador_id: int):
    db.remover_jogador(jogador_id)

# Endpoints - Partidas (Sub-recurso)
@app.post("/jogadores/{jogador_id}/partidas", response_model=Partida, status_code=status.HTTP_201_CREATED)
def registrar_partida(jogador_id: int, entrada: PartidaEntrada, response: Response):
    partida = db.salvar_partida(jogador_id, entrada)
    response.headers["Location"] = f"/partidas/{partida.id}"
    return partida

@app.get("/jogadores/{jogador_id}/partidas", response_model=List[Partida])
def listar_partidas_do_jogador(jogador_id: int):
    return db.listar_partidas_jogador(jogador_id)