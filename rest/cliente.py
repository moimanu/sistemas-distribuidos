import requests
BASE = "http://127.0.0.1:8000"
r = requests.post(
    f"{BASE}/dispositivos",
    json={"nome": "sensor-corredor", "local": "Bloco A"},
    timeout=3,
)

print("POST", r.status_code, r.json())
dispositivo = r.json()
r = requests.get(f"{BASE}/dispositivos/{dispositivo['id']}", timeout=3)

print("GET", r.status_code, r.json())
try:
    requests.get(f"{BASE}/dispositivos", timeout=0.001)
except requests.exceptions.Timeout:
    print("Timeout observado: a chamada remota não tem duração garantida.")