from datetime import datetime, timezone
from typing import Dict, List
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(title="API de Dispositivos", version="1.0")

class DispositivoEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=80)
    local: str = Field(min_length=2, max_length=120)

class Dispositivo(DispositivoEntrada):
    id: int

class LeituraEntrada(BaseModel):
    valor: float
    unidade: str = Field(min_length=1, max_length=16)

class Leitura(LeituraEntrada):
    dispositivo_id: int
    instante: str
    
dispositivos: Dict[int, Dispositivo] = {}
leituras: List[Leitura] = []
proximo_id = 1

@app.get("/dispositivos", response_model=list[Dispositivo])
def listar_dispositivos():
    return list(dispositivos.values())

@app.post("/dispositivos", response_model=Dispositivo, status_code=status.HTTP_201_CREATED)
def criar_dispositivo(entrada: DispositivoEntrada, response: Response):
    global proximo_id
    d = Dispositivo(id=proximo_id, **entrada.model_dump())
    dispositivos[d.id] = d
    proximo_id += 1
    response.headers["Location"] = f"/dispositivos/{d.id}"
    return d

@app.get("/dispositivos/{dispositivo_id}", response_model=Dispositivo)
def obter_dispositivo(dispositivo_id: int):
    d = dispositivos.get(dispositivo_id)
    if not d:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return d

@app.put("/dispositivos/{dispositivo_id}", response_model=Dispositivo)
def substituir_dispositivo(dispositivo_id: int, entrada: DispositivoEntrada):
    if dispositivo_id not in dispositivos:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    d = Dispositivo(id=dispositivo_id, **entrada.model_dump())
    dispositivos[dispositivo_id] = d
    return d

@app.delete("/dispositivos/{dispositivo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_dispositivo(dispositivo_id: int):
    if dispositivo_id not in dispositivos:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    del dispositivos[dispositivo_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/dispositivos/{dispositivo_id}/leituras", response_model=Leitura, status_code=201)
def registrar_leitura(dispositivo_id: int, entrada: LeituraEntrada):
    if dispositivo_id not in dispositivos:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    leitura = Leitura(
        dispositivo_id=dispositivo_id,
        instante=datetime.now(timezone.utc).isoformat(),
        **entrada.model_dump(),
    )
    leituras.append(leitura)
    return leitura

@app.get("/dispositivos/{dispositivo_id}/leituras", response_model=list[Leitura])
def listar_leituras(dispositivo_id: int):
    if dispositivo_id not in dispositivos:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return [l for l in leituras if l.dispositivo_id == dispositivo_id]
