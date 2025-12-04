import paho.mqtt.client as mqtt
import sys

# --- CONFIGURAÇÕES ---
BROKER = "168.138.159.118"  # <--- COLOQUE SEU IP AQUI
PORT = 1883
TOPIC = "teste/caprover"
USUARIO = "admin"      # <--- Coloque o usuário que você criou no terminal
SENHA = "@Senai2026"    # <--- Coloque a senha que você criou

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"[ASSINANTE] Conectado ao servidor {BROKER}!")
        client.subscribe(TOPIC)
        print(f"[ASSINANTE] Ouvindo o tópico: {TOPIC}...")
        print("Pressione CTRL+C para sair.")
    else:
        print(f"[ERRO] Falha ao conectar. Código: {reason_code}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"\n[RECEBIDO] Tópico: {msg.topic}")
    print(f"Mensagem: {payload}")

# Configuração do Cliente
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


client.username_pw_set(USUARIO, SENHA)


client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, 60)
    # loop_forever mantém o script rodando infinitamente esperando mensagens
    client.loop_forever()
except KeyboardInterrupt:
    print("\n[SAINDO] Encerrando assinante...")
    client.disconnect()
except Exception as e:
    print(f"[ERRO] Não foi possível conectar: {e}")