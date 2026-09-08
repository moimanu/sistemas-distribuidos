import json
import time
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Tópicos
TOPIC_FILA = "rocketleague/matchmaking/fila"
TOPIC_STATUS = "rocketleague/jogadores/+/status"
TOPIC_PARTIDA_INFO = "rocketleague/partida/{id_partida}/info"

class Matchmaker:
    def __init__(self):
        self.fila = []
        self.room_counter = 100
        self.seq = 1

        # Suporte a paho-mqtt v2.x e v1.x
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="matchmaker_service")
        except AttributeError:
            self.client = mqtt.Client(client_id="matchmaker_service")

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("⚡ [MATCHMAKER] Conectado ao Broker MQTT com sucesso.")
        client.subscribe([(TOPIC_FILA, 1), (TOPIC_STATUS, 1)])
        print(f"📌 [MATCHMAKER] Inscrito nos tópicos: '{TOPIC_FILA}' (QoS 1) e '{TOPIC_STATUS}' (QoS 1)")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload_raw = msg.payload.decode('utf-8')
        
        try:
            payload = json.loads(payload_raw)
        except json.JSONDecodeError:
            print(f"⚠️ [MATCHMAKER] Payload JSON inválido recebido em {topic}: {payload_raw}")
            return

        # 1. Tratar status de jogador (online/offline)
        if topic.startswith("rocketleague/jogadores/") and topic.endswith("/status"):
            player_id = payload.get("player_id")
            status = payload.get("status")

            if status == "offline" and player_id in self.fila:
                self.fila.remove(player_id)
                print(f"💀 [MATCHMAKER] Jogador '{player_id}' ficou offline/desconectou! Removido da fila. Fila atual: {self.fila}")
            elif status == "online":
                print(f"🟢 [MATCHMAKER] Jogador '{player_id}' está online.")

        # 2. Tratar pedido de entrada na fila
        elif topic == TOPIC_FILA:
            player_id = payload.get("player_id")
            action = payload.get("action")

            if action == "busca_partida" and player_id:
                if player_id not in self.fila:
                    self.fila.append(player_id)
                    print(f"🎮 [MATCHMAKER] Jogador '{player_id}' entrou na fila. Fila atual: {self.fila}")
                else:
                    print(f"ℹ️ [MATCHMAKER] Jogador '{player_id}' já está na fila.")

                self.verificar_e_criar_partida()

    def verificar_e_criar_partida(self):
        if len(self.fila) >= 2:
            p1 = self.fila.pop(0)
            p2 = self.fila.pop(0)
            
            self.room_counter += 1
            id_partida = str(self.room_counter)
            
            info_topic = TOPIC_PARTIDA_INFO.format(id_partida=id_partida)
            room_payload = {
                "id_partida": id_partida,
                "jogadores": [p1, p2],
                "status": "criada",
                "producer": "matchmaker",
                "seq": self.seq
            }
            self.seq += 1

            # Publica a confirmação de sala com Retain=True e QoS 1
            self.client.publish(info_topic, json.dumps(room_payload), qos=1, retain=True)
            print(f"🚀 [MATCHMAKER] PARTIDA CRIADA! Sala #{id_partida} -> Jogadores: [{p1}, {p2}] | Tópico: '{info_topic}' (Retained=True, QoS 1)")

    def start(self):
        self.client.connect(BROKER_HOST, BROKER_PORT, 60)
        print("🔄 [MATCHMAKER] Iniciando loop do Matchmaker...")
        self.client.loop_forever()

if __name__ == "__main__":
    matchmaker = Matchmaker()
    matchmaker.start()
