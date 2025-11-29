import paho.mqtt.client as mqtt
import time
import sys

# --- CONFIGURAÇÕES ---
# Coloque aqui o IP do seu servidor CapRover (NÃO use https://...)
BROKER = "168.138.159.118" 
PORT = 1883
TOPIC = "teste/caprover"

# --- FUNÇÕES DE CALLBACK ---

def on_connect(client, userdata, flags, reason_code, properties=None):
    """Chamado quando o servidor responde à tentativa de conexão."""
    if reason_code == 0:
        print(f"[SUCESSO] Conectado ao Broker em {BROKER}!")
        # Assim que conectar, assinamos o tópico para ouvir mensagens
        client.subscribe(TOPIC)
        print(f"[INFO] Assinado no tópico: {TOPIC}")
    else:
        print(f"[ERRO] Falha ao conectar. Código de retorno: {reason_code}")
        sys.exit(1)

def on_message(client, userdata, msg):
    """Chamado quando uma mensagem é recebida."""
    payload = msg.payload.decode()
    print("------------------------------------------------")
    print(f"[MENSAGEM RECEBIDA]")
    print(f"Tópico: {msg.topic}")
    print(f"Conteúdo: {payload}")
    print("------------------------------------------------")

# --- CONFIGURAÇÃO DO CLIENTE ---

# Usando a versão mais recente da API do Paho MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

print(f"Tentando conectar em {BROKER}:{PORT} ...")

try:
    # Conecta ao broker
    client.connect(BROKER, PORT, 60)
except Exception as e:
    print(f"[ERRO CRÍTICO] Não foi possível alcançar o servidor: {e}")
    print("DICA: Verifique se a porta 1883 está liberada no Firewall da sua VPS.")
    sys.exit(1)

# Inicia o loop em background para processar rede
client.loop_start()

# Espera um pouco para garantir a conexão
time.sleep(2)

# --- ENVIANDO TESTE ---
mensagem = "Funciona! O Mosquito está vivo no CapRover."
print(f"[ENVIANDO] Publicando mensagem: '{mensagem}'")
client.publish(TOPIC, mensagem)

# Mantém o script rodando por mais 5 segundos para dar tempo de receber a resposta
time.sleep(5)

# Encerra
client.loop_stop()
client.disconnect()
print("Teste finalizado.")