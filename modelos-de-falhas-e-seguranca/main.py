import random
import time
from typing import Dict, List, Optional
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Header, Response, status, Depends
from pydantic import BaseModel, Field

app = FastAPI(
    title="API de Estatísticas - Laboratório de Falhas e Segurança",
    version="2.0-lab"
)

# CONTROLE DE SEGURANÇA (Chave de API / Token estático)
TOKEN_VALIDO = "secret-token-123"

def verificar_autenticacao(x_api_token: Optional[str] = Header(None)):
    """Controle de Segurança: Validação de Token no Header HTTP."""
    if x_api_token != TOKEN_VALIDO:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autorizado: Token de API inválido ou ausente."
        )
    return x_api_token


# MODELOS DE DADOS
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


# BANCO DE DADOS EM MEMÓRIA COM SUPORTE A IDEMPOTENCY KEY
class Database:
    def __init__(self):
        self.jogadores: Dict[int, Jogador] = {}
        self.partidas: Dict[int, Partida] = {}
        self.idempotency_keys: Dict[str, dict] = {}
        self._id_jogador = 0
        self._id_partida = 0
        self._seed()

    def _seed(self):
        self.salvar_jogador(JogadorEntrada(nickname="Fennec", plataforma="PC", rank="Grand Champion"))
        self.salvar_jogador(JogadorEntrada(nickname="Breakout", plataforma="PlayStation", rank="Gold"))

    def salvar_jogador(self, entrada: JogadorEntrada) -> Jogador:
        for j in self.jogadores.values():
            if j.nickname.lower() == entrada.nickname.lower():
                raise HTTPException(status_code=409, detail=f"Nickname '{entrada.nickname}' já existe.")
        self._id_jogador += 1
        jogador = Jogador(id=self._id_jogador, **entrada.model_dump())
        self.jogadores[self._id_jogador] = jogador
        return jogador

    def salvar_partida_com_idempotencia(self, jogador_id: int, entrada: PartidaEntrada, idempotency_key: Optional[str] = None) -> Partida:
        if jogador_id not in self.jogadores:
            raise HTTPException(status_code=404, detail="Jogador não encontrado")
        
        if idempotency_key and idempotency_key in self.idempotency_keys:
            return self.idempotency_keys[idempotency_key]["resposta"]

        self._id_partida += 1
        partida = Partida(
            id=self._id_partida,
            jogador_id=jogador_id,
            instante=datetime.now(timezone.utc).isoformat(),
            **entrada.model_dump()
        )
        self.partidas[self._id_partida] = partida

        if idempotency_key:
            self.idempotency_keys[idempotency_key] = {"resposta": partida}

        return partida

db = Database()


# ROTAS NORMAIS DA API (COM SEGURANÇA APLICADA)
@app.get("/jogadores", response_model=List[Jogador])
def listar_jogadores():
    return list(db.jogadores.values())

@app.post("/jogadores", response_model=Jogador, status_code=status.HTTP_201_CREATED)
def criar_jogador(entrada: JogadorEntrada, token: str = Depends(verificar_autenticacao)):
    return db.salvar_jogador(entrada)

@app.post("/jogadores/{jogador_id}/partidas", response_model=Partida, status_code=status.HTTP_201_CREATED)
def registrar_partida(
    jogador_id: int, 
    entrada: PartidaEntrada, 
    x_idempotency_key: Optional[str] = Header(None),
    token: str = Depends(verificar_autenticacao)
):
    return db.salvar_partida_com_idempotencia(jogador_id, entrada, x_idempotency_key)


# ROTAS DE EXPERIMENTOS DE FALHAS CONTROLADAS (LABORATÓRIO)
@app.get("/experimento/instavel")
def experimento_instavel(atraso_ms: int = 0, prob_falha: float = 0.0):
    if atraso_ms > 0:
        time.sleep(atraso_ms / 1000.0)
    
    if random.random() < prob_falha:
        raise HTTPException(status_code=503, detail="Falha transitória injetada (Servidor Indisponível)")
    
    return {"status": "ok", "atraso_ms": atraso_ms, "prob_falha": prob_falha}