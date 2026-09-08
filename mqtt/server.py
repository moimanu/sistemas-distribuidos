import json
import time
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
ID_PARTIDA = "101"

TOPIC_ESTADO = f"rocketleague/partida/{ID_PARTIDA}/estado"
TOPIC_EVENTOS = f"rocketleague/partida/{ID_PARTIDA}/eventos"

class MatchServer:
    def __init__(self):
        self.seq = 1
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="match_server_101")
        except AttributeError:
            self.client = mqtt.Client(client_id="match_server_101")

    def get_next_seq(self):
        current = self.seq
        self.seq += 1
        return current

    def start(self):
        self.client.connect(BROKER_HOST, BROKER_PORT, 60)
        self.client.loop_start()
        print(f"⚡ [SERVER/JUIZ] Conectado ao Broker. Gerenciando Partida #{ID_PARTIDA}...")

        time.sleep(1)

        # 1. Definir o estado inicial da partida (Retained=True, QoS 1)
        placar = {"time_azul": 0, "time_laranja": 0}
        estado_payload = json.dumps({
            "id_partida": ID_PARTIDA,
            "status": "EM_ANDAMENTO",
            "placar": placar,
            "tempo_restante_seg": 300,
            "producer": "server",
            "seq": self.get_next_seq()
        })
        self.client.publish(TOPIC_ESTADO, estado_payload, qos=1, retain=True)
        print(f"📌 [SERVER/JUIZ] Estado inicial publicado em '{TOPIC_ESTADO}' (Retained=True, QoS 1): Placar 0x0")

        time.sleep(2)

        # 2. Simular Evento Crítico de GOL (QoS 2 - Entrega Exata Garantida)
        gol_payload = json.dumps({
            "id_partida": ID_PARTIDA,
            "evento": "GOL!",
            "autor": "p1",
            "time": "time_azul",
            "descricao": "Golaço de bicicleta no ângulo!",
            "producer": "server",
            "seq": self.get_next_seq()
        })
        self.client.publish(TOPIC_EVENTOS, gol_payload, qos=2, retain=False)
        print(f"⚽ [SERVER/JUIZ] EVENTO DE GOL publicado em '{TOPIC_EVENTOS}' com QoS 2 (Garantia de entrega sem perda/duplicação)!")

        time.sleep(1)

        # 3. Atualizar Estado Retido com o novo placar (Retained=True, QoS 1)
        placar["time_azul"] = 1
        estado_atualizado_payload = json.dumps({
            "id_partida": ID_PARTIDA,
            "status": "EM_ANDAMENTO",
            "placar": placar,
            "tempo_restante_seg": 210,
            "producer": "server",
            "seq": self.get_next_seq()
        })
        self.client.publish(TOPIC_ESTADO, estado_atualizado_payload, qos=1, retain=True)
        print(f"📌 [SERVER/JUIZ] Estado do placar atualizado em '{TOPIC_ESTADO}' (Retained=True, QoS 1): Placar 1x0")

        time.sleep(2)

        # 4. Simular Fim de Jogo (QoS 2)
        fim_payload = json.dumps({
            "id_partida": ID_PARTIDA,
            "evento": "FIM_DE_JOGO",
            "vencedor": "time_azul",
            "placar_final": placar,
            "producer": "server",
            "seq": self.get_next_seq()
        })
        self.client.publish(TOPIC_EVENTOS, fim_payload, qos=2, retain=False)
        print(f"🏁 [SERVER/JUIZ] Evento de FIM DE JOGO publicado em '{TOPIC_EVENTOS}' com QoS 2!")

        time.sleep(1)
        self.client.loop_stop()
        self.client.disconnect()
        print("✅ [SERVER/JUIZ] Execução encerrada com sucesso.")

if __name__ == "__main__":
    server = MatchServer()
    server.start()
