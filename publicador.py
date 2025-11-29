import paho.mqtt.client as mqtt
import time
import random

# --- CONFIGURAÇÕES ---
BROKER = "168.138.159.118" # <--- COLOQUE SEU IP AQUI
PORT = 1883
TOPIC = "teste/caprover"
USUARIO = "admin"      # <--- Coloque o usuário que você criou no terminal
SENHA = "@Senai2026"    # <--- Coloque a senha que você criou

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

try:

    # --- AQUI ESTÁ A MUDANÇA ---
    client.username_pw_set(USUARIO, SENHA)
    # ---------------------------
    
    client.connect(BROKER, PORT, 60)
    client.loop_start() # Inicia loop em background
    
    print(f"[PUBLICADOR] Conectado! Enviando dados para '{TOPIC}'...")

    contador = 1
    while True:
        temperatura = random.randint(20, 30)
        mensagem = f"Mensagem #{contador} - Temperatura: {temperatura}°C"
        
        info = client.publish(TOPIC, mensagem)
        info.wait_for_publish() # Garante que enviou
        
        print(f"[ENVIADO] {mensagem}")
        
        contador += 1
        time.sleep(1) # Espera 3 segundos antes da próxima

except KeyboardInterrupt:
    print("\n[SAINDO] Parando publicador...")
    client.loop_stop()
    client.disconnect()
except Exception as e:
    print(f"[ERRO] Falha na conexão: {e}")