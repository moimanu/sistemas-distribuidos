import hashlib
import json
import copy
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class TradeEvent:
    sender: str
    receiver: str
    item: str

    def to_dict(self) -> Dict[str, str]:
        return {"sender": self.sender, "receiver": self.receiver, "item": self.item}

@dataclass
class Block:
    index: int
    data: dict
    previous_hash: str
    hash: str = ""

    def calculate_hash(self) -> str:
        block_content = {
            "index": self.index,
            "data": self.data,
            "previous_hash": self.previous_hash
        }
        raw_bytes = json.dumps(block_content, sort_keys=True).encode('utf-8')
        return hashlib.sha256(raw_bytes).hexdigest()

class RocketLeagueLedger:
    def __init__(self):
        self.chain: List[Block] = []
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        genesis = Block(index=0, data={"info": "Psyonix Genesis Block"}, previous_hash="0" * 64)
        genesis.hash = genesis.calculate_hash()
        self.chain.append(genesis)

    def add_block(self, trade: TradeEvent) -> None:
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            data=trade.to_dict(),
            previous_hash=previous_block.hash
        )
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def validate(self) -> Tuple[bool, str]:
        for i, block in enumerate(self.chain):
            if block.hash != block.calculate_hash():
                return False, f"Hash inválido no bloco {i}"
            if i > 0 and block.previous_hash != self.chain[i - 1].hash:
                return False, f"Ligação quebrada no bloco {i}"
        return True, "Cadeia válida"

def main():
    ledger = RocketLeagueLedger()
    
    trades = [
        ("Fnx", "BDS", "Titanium White Octane"),
        ("Zen", "Vatira", "Alpha Boost"),
        ("MonkeyMoon", "Seikoo", "Fennec"),
        ("GarrettG", "Jstn", "Zomba Wheels"),
        ("Squishy", "Gimmick", "Dominus"),
        ("FairyPeak", "Kaydop", "Batmobile"),
        ("Turbopolsa", "Panda", "Gold Rush"),
        ("Chicago", "Knaps", "Dueling Dragons"),
        ("Atomic", "Daniel", "Mainframe"),
        ("BeastMode", "Comm", "Cristiano Wheels"),
        ("AyyJayy", "Retals", "Halo Topper"),
        ("Sypical", "Arsenal", "Standard Boost"),
        ("Joyo", "Rise", "Dieci Black"),
        ("Firstkiller", "Mist", "Reaper Goal Explosion"),
        ("AppJack", "Noly", "Octane ZSR"),
        ("Chronic", "Lj", "FSL Wheels"),
        ("Yanxnz", "Lostt", "Bubbly Decal"),
        ("Kv1", "Aztromick", "Slipstream"),
        ("NisQ", "Droppz", "Heatwave")
    ]
    
    for sender, receiver, item in trades:
        ledger.add_block(TradeEvent(sender, receiver, item))
        
    print("=== ESTADO INICIAL ===")
    valid, msg = ledger.validate()
    print(msg)
    print(f"Total de blocos: {len(ledger.chain)}")
    print(f"Hash Bloco 5 Original: {ledger.chain[5].hash}\n")

    print("=== ADULTERAÇÃO SEM RECÁLCULO ===")
    ledger.chain[5].data["item"] = "Fake Alpha Boost"
    valid, msg = ledger.validate()
    print(f"Validação: {msg}")
    print(f"Hash Bloco 5 atual: {ledger.chain[5].hash}\n")

    print("=== ADULTERAÇÃO COM RECÁLCULO (FORGE) ===")
    for i in range(5, len(ledger.chain)):
        if i > 0:
            ledger.chain[i].previous_hash = ledger.chain[i-1].hash
        ledger.chain[i].hash = ledger.chain[i].calculate_hash()
    
    valid, msg = ledger.validate()
    print(f"Validação após recalcular tudo: {msg}")
    print(f"Novo Hash Bloco 5: {ledger.chain[5].hash}")
    print(f"Novo Hash Bloco 6 (afetado em cascata): {ledger.chain[6].hash}\n")

    print("=== RÉPLICAS DIVERGENTES ===")
    replica_a = copy.deepcopy(ledger)
    replica_b = copy.deepcopy(ledger)

    replica_a.add_block(TradeEvent("Player1", "Player2", "Mantis"))
    replica_b.add_block(TradeEvent("Player3", "Player4", "Endo"))
    
    print(f"Hash topo Réplica A (Bloco 20): {replica_a.chain[-1].hash}")
    print(f"Hash topo Réplica B (Bloco 20): {replica_b.chain[-1].hash}")

if __name__ == '__main__':
    main()