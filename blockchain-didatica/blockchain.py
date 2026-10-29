import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import List, Dict

@dataclass
class Block:
    index: int
    timestamp: str
    data: dict
    previous_hash: str
    nonce: int = 0
    hash: str = ""

    def calculate_hash(self) -> str:
        """Calcula o hash SHA-256 do bloco."""
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(raw).hexdigest()

class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain: List[Block] = [self._create_genesis_block()]

    def _create_genesis_block(self) -> Block:
        """Cria o bloco inicial (gênese) da cadeia."""
        b = Block(index=0, timestamp="GENESIS", data={"msg": "genesis"}, previous_hash="0" * 64)
        b.hash = b.calculate_hash()
        return b

    def mine(self, data: dict) -> Block:
        """Realiza o Proof of Work para encontrar um hash válido e minera o bloco."""
        new_index = len(self.chain)
        timestamp = datetime.now(timezone.utc).isoformat()
        previous_hash = self.chain[-1].hash
        
        b = Block(index=new_index, timestamp=timestamp, data=data, previous_hash=previous_hash)
        target = "0" * self.difficulty

        while True:
            b.hash = b.calculate_hash()
            if b.hash.startswith(target):
                break
            b.nonce += 1
            
        self.chain.append(b)
        return b

    def is_chain_valid(self, chain_to_check: List[Block] = None) -> bool:
        """Valida se uma cadeia de blocos é íntegra (hashes conferem e PoW é válido)."""
        chain = chain_to_check if chain_to_check is not None else self.chain
        target = "0" * self.difficulty

        for i, b in enumerate(chain):
            # 1. Verifica se o hash salvo condiz com os dados
            if b.hash != b.calculate_hash():
                return False
            
            # 2. Verifica a ligação com o bloco anterior
            if i > 0:
                if b.previous_hash != chain[i-1].hash:
                    return False
            
            # 3. Verifica se a dificuldade do PoW foi respeitada
            if not b.hash.startswith(target):
                return False
                
        return True

    @classmethod
    def from_dict_list(cls, chain_dicts: List[Dict], difficulty: int) -> 'Blockchain':
        """Reconstrói uma instância de Blockchain a partir de uma lista de dicionários (útil para rede)."""
        bc = cls(difficulty=difficulty)
        bc.chain = [Block(**b_dict) for b_dict in chain_dicts]
        return bc