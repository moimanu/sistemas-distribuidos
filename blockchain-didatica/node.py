from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from typing import List

from blockchain import Blockchain, Block

app = FastAPI()
DIFFICULTY = 3
bc = Blockchain(difficulty=DIFFICULTY)
peers = set()

class DataPayload(BaseModel):
    origem: str
    destino: str
    valor: float

class PeerPayload(BaseModel):
    url: str

@app.get("/chain")
def get_chain():
    """Retorna a cadeia atual e seu tamanho."""
    return {
        "length": len(bc.chain), 
        "is_valid": bc.is_chain_valid(),
        "chain": [b.__dict__ for b in bc.chain]
    }

@app.post("/mine")
def mine_block(data: DataPayload):
    """Minera um novo bloco com os dados fornecidos."""
    b = bc.mine(data.model_dump())
    return b.__dict__

@app.post("/peers")
def add_peer(peer: PeerPayload):
    """Adiciona um nó vizinho para sincronização."""
    peers.add(peer.url.rstrip("/"))
    return {"peers": sorted(peers)}

@app.post("/tamper")
def tamper_chain():
    """Simula uma adulteração proposital para fins didáticos."""
    if len(bc.chain) < 2:
        raise HTTPException(status_code=400, detail="Minere pelo menos 1 bloco antes de adulterar.")
    
    # Adultera o dado do primeiro bloco minerado sem refazer o hash
    bc.chain[1].data["valor"] = 99999.0
    return {"message": "Cadeia adulterada propositalmente. Chame /chain para ver a invalidade."}

@app.get("/resolve")
def resolve_conflicts():
    """
    Reconciliação: Busca a cadeia dos vizinhos.
    Adota a cadeia mais longa, DESDE QUE ela seja válida estruturalmente.
    """
    global bc
    longest_chain = bc.chain
    max_length = len(bc.chain)
    replaced = False

    for peer in peers:
        try:
            response = requests.get(f"{peer}/chain", timeout=2)
            if response.status_code == 200:
                data = response.json()
                peer_length = data["length"]
                peer_chain_dicts = data["chain"]

                # Regra: Só avalia se for estritamente maior
                if peer_length > max_length:
                    # Reconstrói a cadeia recebida para validar
                    peer_bc = Blockchain.from_dict_list(peer_chain_dicts, DIFFICULTY)
                    
                    # Validação forte antes de adotar
                    if peer_bc.is_chain_valid():
                        max_length = peer_length
                        longest_chain = peer_bc.chain
                        replaced = True
        except requests.RequestException:
            # Ignora peer indisponível (resiliência)
            continue

    if replaced:
        bc.chain = longest_chain
        return {"message": "Cadeia substituída por uma válida e mais longa da rede.", "length": max_length}
    
    return {"message": "Cadeia local mantida (é a mais longa ou a única válida).", "length": len(bc.chain)}