import time
import threading
import paho.mqtt.client as mqtt
from collections import deque, defaultdict

# Armazena para cada sensor (topic) uma fila de no máximo 2 temperaturas
sensor_temperatures = defaultdict(lambda: deque(maxlen=2))

# Variável global para armazenar a última média calculada
last_avg = None

# Lock para acesso seguro às temperaturas entre threads
data_lock = threading.Lock()

# Cria cliente MQTT
client = mqtt.Client()

# Callback para quando conectar ao broker
def on_connect(client, userdata, flags, rc):
    print("[CAT] Conectado ao broker")
    client.subscribe("sensors/temperature/#")

# Callback para quando uma nova mensagem é recebida
def on_message(client, userdata, msg):
    try:
        # Extrai o sensor_id do tópico
        topic_parts = msg.topic.split('/')
        if len(topic_parts) != 3:
            print(f"[CAT] Tópico inválido: {msg.topic}")
            return

        sensor_id = topic_parts[2]

        # Converte temperatura recebida
        temp = float(msg.payload.decode())

        # Adiciona à fila do sensor correspondente
        with data_lock:
            sensor_temperatures[sensor_id].append(temp)

    except ValueError:
        print("[CAT] Valor inválido recebido.")

# Função para calcular e publicar médias a cada 1 segundo
def monitor_temperature():
    global last_avg

    while True:
        time.sleep(1)
        with data_lock:
            latest_temps = [temps[-1] for temps in sensor_temperatures.values() if temps]

        if len(latest_temps) >= 2:
            current_avg = sum(latest_temps) / len(latest_temps)
            print(f"[CAT] Média atual entre sensores: {current_avg:.2f}")

            if last_avg is not None and abs(current_avg - last_avg) >= 5:
                client.publish("events/sudden_change", f"{current_avg:.2f}")
                print("[CAT] 🔺 Mudança repentina de temperatura!")

            if current_avg > 200:
                client.publish("events/high_temperature", f"{current_avg:.2f}")
                print("[CAT] 🔥 Temperatura alta!")

            last_avg = current_avg

# Define os callbacks
client.on_connect = on_connect
client.on_message = on_message

# Conecta ao broker
client.connect("localhost", 1883, 60)

# Inicia thread de monitoramento
monitor_thread = threading.Thread(target=monitor_temperature, daemon=True)
monitor_thread.start()

# Loop principal MQTT
client.loop_forever()
