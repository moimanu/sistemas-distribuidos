# BIBLIOTECAS NECESSÁRIAS: pip install pyyaml toml

import csv
import io
import json
import socket
import xml.etree.ElementTree as ET
import toml
import yaml

# FUNÇÕES DE DESSERIALIZAÇÃO (Recebem string e retornam dicionário)

def deserialize_csv(texto):
  f = io.StringIO(texto.strip())
  return next(csv.DictReader(f))

def deserialize_json(texto):
  return json.loads(texto)

def deserialize_xml(texto):
  root = ET.fromstring(texto)
  return {
      "nome": root.find("nome").text,
      "cpf": root.find("cpf").text,
      "idade": root.find("idade").text,
      "mensagem": root.find("mensagem").text,
  }

def deserialize_yaml(texto):
  return yaml.safe_load(texto)


def deserialize_toml(texto):
  return toml.loads(texto)

# EXIBIÇÃO DOS DADOS

def exibir_dados(dados, formato):
  print(f"\nRECEBIDO EM {formato}:")
  print(f"Nome:     {dados['nome']}")
  print(f"CPF:      {dados['cpf']}")
  print(f"Idade:    {dados['idade']}")
  print(f"Mensagem: {dados['mensagem']}")

# LÓGICA DE REDE DO SERVIDOR

def rodar_servidor():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(("127.0.0.1", 5000))
  s.listen(1)
  print("\nSERVIDOR AGUARDANDO CONEXÃO...")

  conn, _ = s.accept()

  formatos = [
      ("CSV", deserialize_csv),
      ("JSON", deserialize_json),
      ("XML", deserialize_xml),
      ("YAML", deserialize_yaml),
      ("TOML", deserialize_toml),
  ]

  for formato, funcao_desserializar in formatos:
    texto = conn.recv(1024).decode("utf-8")
    if not texto:
      break

    dados = funcao_desserializar(texto)
    exibir_dados(dados, formato)

  conn.close()
  s.close()

if __name__ == "__main__":
  rodar_servidor()