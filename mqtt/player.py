import sys
import json
import time
import random
import signal
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883

class PlayerClient:
    def __init__(self, player_id):
        self.player_id = player_id
        self.seq = 1
        self.id_partida_alocada = None
        self.em_partida = False

        # Tópicos específicos do jogador
        self.topic_status = f"rocketleague/jogadores/{self.player_id}/status"
        self.topic_fila = "rocketleague/matchmaking/fila"
        self.topic_partida_info = "rocketleague/partida/+/info"

        # Configura cliente MQTT
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"player_{self.player_id}")
        except AttributeError:
            self.client = mqtt.Client(client_id=f"player_{self.player_id}")

        # Configurar LAST WILL AND TESTAMENT (LWT) antes de conectar
        lwt_payload = json.dumps({
            "player_id": self.player_id,
            "status": "offline",
            "reason": "LWT_DISCONNECT",
            "producer": self.player_id,
            "seq": self.seq
        })
        self.client.will_set(self.topic_status, lwt_payload, qos=1, retain=True)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def get_next_seq(self):
        current = self.seq
        self.seq += 1
        return current

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"⚡ [PLAYER: {self.player_id}] Conectado ao Broker MQTT.")
        
        # 1. Publica status ONLINE (Retained=True, QoS 1)
        online_payload = json.dumps({
            "player_id": self.player_id,
            "status": "online",
            "producer": self.player_id,
            "seq": self.get_next_seq()
        })
        client.publish(self.topic_status, online_payload, qos=1, retain=True)
        print(f"🟢 [PLAYER: {self.player_id}] Status 'online' publicado (Retained=True, QoS 1).")

        # 2. Entra na fila de matchmaking (QoS 1)
        fila_payload = json.dumps({
            "player_id": self.player_id,
            "action": "busca_partida",
            "producer": self.player_id,
            "seq": self.get_next_seq()
        })
        client.publish(self.topic_fila, fila_payload, qos=1, retain=False)
        print(f"🎯 [PLAYER: {self.player_id}] Pedido de busca de partida enviado para a fila (QoS 1).")

        # 3. Assina confirmação de sala
        client.subscribe(self.topic_partida_info, qos=1)
        print(f"📌 [PLAYER: {self.player_id}] Aguardando confirmação de partida em '{self.topic_partida_info}'...")

    def on_message(self, client, userdata, msg):
        payload_raw = msg.payload.decode('utf-8')
        try:
            payload = json.loads(payload_raw)
        except json.JSONDecodeError:
            return

        # Verifica se é confirmação de sala e se este jogador está alocado
        jogadores = payload.get("jogadores", [])
        id_partida = payload.get("id_partida")

        if self.player_id in jogadores and not self.em_partida:
            self.id_partida_alocada = id_partida
            self.em_partida = True
            print(f"🎉 [PLAYER: {self.player_id}] PARTIDA ENCONTRADA! Alocado na Sala #{id_partida} com {jogadores}")
            self.iniciar_streaming_telemetria()

    def iniciar_streaming_telemetria(self):
        topic_telemetria = f"rocketleague/partida/{self.id_partida_alocada}/telemetria"
        print(f"🏎️ [PLAYER: {self.player_id}] Iniciando streaming de telemetria (QoS 0) em '{topic_telemetria}'...")

        for i in range(1, 11):
            if not self.em_partida:
                break
            
            velocidade = round(random.uniform(40.0, 120.0), 1)
            boost = random.randint(0, 100)
            
            telemetria_payload = json.dumps({
                "player_id": self.player_id,
                "id_partida": self.id_partida_alocada,
                "pacote": i,
                "velocidade_kmh": velocidade,
                "boost_pct": boost,
                "producer": self.player_id,
                "seq": self.get_next_seq()
            })

            # Envio em alta frequência com QoS 0 (sem confirmação de entrega)
            self.client.publish(topic_telemetria, telemetria_payload, qos=0, retain=False)
            print(f"📊 [PLAYER: {self.player_id}] Telemetria #{i}/10 enviada | Vel: {velocidade}km/h | Boost: {boost}% (QoS 0)")
            time.sleep(0.5)

        print(f"✅ [PLAYER: {self.player_id}] Streaming de telemetria concluído com sucesso!")

    def start(self):
        self.client.connect(BROKER_HOST, BROKER_PORT, 60)
        
        # Inicia loop em background para responder a mensagens
        self.client.loop_start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n💥 [PLAYER: {self.player_id}] Queda simulada por Ctrl+C! Encerrando processo abruptamente para acionar LWT no Broker...")
            import os
            os._exit(1)

if __name__ == "__main__":
    player_id = sys.argv[1] if len(sys.argv) > 1 else "p1"
    player = PlayerClient(player_id)
    player.start()
