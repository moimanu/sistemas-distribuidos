import json
import datetime
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC_WILDCARD = "rocketleague/#"

# Cores ANSI para formatar o dashboard no terminal
COLOR_RESET = "\033[0m"
COLOR_TITLE = "\033[1;36m"
COLOR_TOPIC = "\033[1;33m"
COLOR_PRODUCER = "\033[1;35m"
COLOR_WARN = "\033[1;31m"
COLOR_RETAIN = "\033[1;32m"
COLOR_LWT = "\033[1;41;37m"

class DashboardAuditor:
    def __init__(self):
        # Dicionário para rastrear número de sequência (seq) por produtor
        self.last_seq_per_producer = {}

        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="dashboard_auditor")
        except AttributeError:
            self.client = mqtt.Client(client_id="dashboard_auditor")

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"\n{COLOR_TITLE}======================================================================{COLOR_RESET}")
        print(f"{COLOR_TITLE}🖥️  DASHBOARD & AUDITORIA DE PROTOCOLO MQTT - ROCKET LEAGUE{COLOR_RESET}")
        print(f"{COLOR_TITLE}======================================================================{COLOR_RESET}")
        print(f"⚡ [DASHBOARD] Conectado ao Broker MQTT.")
        
        # Assina todo o ecossistema com QoS 2 para auditar sem perder mensagens
        client.subscribe(TOPIC_WILDCARD, qos=2)
        print(f"📌 [DASHBOARD] Assinado no tópico wildcard '{TOPIC_WILDCARD}' com QoS 2.\n")

    def on_message(self, client, userdata, msg):
        now = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        topic = msg.topic
        qos = msg.qos
        retained = msg.retain
        payload_raw = msg.payload.decode('utf-8')

        try:
            payload = json.loads(payload_raw)
        except json.JSONDecodeError:
            payload = {"raw": payload_raw}

        # Identificar produtor e sequência
        producer = payload.get("producer") or payload.get("player_id") or "desconhecido"
        seq = payload.get("seq")

        # Análise de Flags (Retained & Last Will)
        flags_str = ""
        if retained:
            flags_str += f" {COLOR_RETAIN}[📌 RETAINED]{COLOR_RESET}"
        
        # Detectar Last Will / Desconexão
        is_lwt = (payload.get("reason") == "LWT_DISCONNECT") or (payload.get("status") == "offline" and not payload.get("voluntary", False))
        if is_lwt or "LWT" in payload_raw:
            flags_str += f" {COLOR_LWT}[💀 LAST WILL]{COLOR_RESET}"

        # Análise de Integridade de Sequência (Validação de Protocolo)
        seq_status = ""
        if seq is not None and producer != "desconhecido":
            last_seq = self.last_seq_per_producer.get(producer)
            
            if last_seq is not None:
                if seq > last_seq + 1:
                    seq_status = f" {COLOR_WARN}[🚨 PERDA: seq saltou de {last_seq} para {seq}]{COLOR_RESET}"
                elif seq <= last_seq:
                    seq_status = f" {COLOR_WARN}[⚠️ DUPLICADA: seq {seq} <= último {last_seq}]{COLOR_RESET}"
            
            self.last_seq_per_producer[producer] = seq

        seq_fmt = f" | seq: {seq}" if seq is not None else ""

        # Impressão formatada no console
        print(f"[{now}] Tópico: {COLOR_TOPIC}{topic}{COLOR_RESET} | QoS: {qos}{flags_str}{seq_status}")
        print(f"         Produtor: {COLOR_PRODUCER}{producer}{COLOR_RESET}{seq_fmt}")
        print(f"         Dados: {payload}\n" + "-" * 70)

    def start(self):
        self.client.connect(BROKER_HOST, BROKER_PORT, 60)
        self.client.loop_forever()

if __name__ == "__main__":
    dashboard = DashboardAuditor()
    dashboard.start()
