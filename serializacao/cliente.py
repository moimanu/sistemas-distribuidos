# BIBLIOTECAS NECESSÁRIAS: pip install pyyaml toml

import csv
import io
import json
import socket
import time
import xml.etree.ElementTree as ET
import toml
import yaml

# FUNÇÕES DE SERIALIZAÇÃO (Recebem dicionário e retornam string)

def serialize_csv(d):
  out = io.StringIO()
  w = csv.DictWriter(out, fieldnames=d.keys())
  w.writeheader()
  w.writerow(d)
  return out.getvalue()

def serialize_json(d):
  return json.dumps(d)

def serialize_xml(d):
  root = ET.Element("dados")
  for chave, valor in d.items():
    ET.SubElement(root, chave).text = str(valor)
  return ET.tostring(root, encoding="utf-8").decode("utf-8")

def serialize_yaml(d):
  return yaml.dump(d)

def serialize_toml(d):
  return toml.dumps(d)

# FUNÇÃO DE INTERAÇÃO VIA TERMINAL

def coletar_dados_usuario():
  print("\nPREENCHA OS DADOS PARA ENVIO:")
  nome = input("Nome: ").strip()
  cpf = input("CPF: ").strip()
  idade = input("Idade: ").strip()
  mensagem = input("Mensagem: ").strip()

  return {"nome": nome, "cpf": cpf, "idade": idade, "mensagem": mensagem}

# LÓGICA DE REDE DO CLIENTE

def rodar_cliente():
  dados = coletar_dados_usuario()

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(("127.0.0.1", 5000))

  mensagens = [
      ("CSV", serialize_csv(dados)),
      ("JSON", serialize_json(dados)),
      ("XML", serialize_xml(dados)),
      ("YAML", serialize_yaml(dados)),
      ("TOML", serialize_toml(dados)),
  ]

  for formato, msg in mensagens:
    print(f"\nEnviando dados no formato {formato}:")
    print(msg.strip())  # Imprime o conteúdo gerado pela serialização
    s.sendall(msg.encode("utf-8"))
    time.sleep(0.5)

  s.close()
  print("\nTodas as 5 mensagens foram enviadas com sucesso!")

if __name__ == "__main__":
  rodar_cliente()