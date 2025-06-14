import time
import random
import threading
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
NUM_SENSORS = 10

def sensor_simulation(sensor_id):
    client = mqtt.Client()
    connected = False

    # Atraso inicial aleatório entre 1 e 60 segundos
    start_delay = random.randint(1, 60)
    print(f"[{sensor_id}] ⏳ Iniciando em {start_delay}s...")
    time.sleep(start_delay)

    while True:
        # 10% de chance de "falhar" (desconectar)
        if connected and random.random() < 0.1:
            print(f"[{sensor_id}] ❌ Simulando falha de conexão...")
            client.disconnect()
            connected = False
            time.sleep(random.randint(5, 15))  # Tempo "fora do ar"

        # Tenta conectar se não estiver conectado
        if not connected:
            try:
                client.connect(BROKER, PORT, 60)
                connected = True
                print(f"[{sensor_id}] ✅ Reconectado ao broker")
            except Exception as e:
                print(f"[{sensor_id}] Falha ao conectar: {e}")
                time.sleep(5)
                continue

        # Se conectado, publica temperatura
        temperature = random.uniform(150, 240)
        topic = f"sensors/temperature/{sensor_id}"
        client.publish(topic, temperature)
        print(f"[{sensor_id}] 📡 Enviou temperatura: {temperature:.2f}")

        time.sleep(60)

# Cria uma thread para cada sensor
threads = []
for i in range(NUM_SENSORS):
    sensor_id = f"sensor{i+1}"
    t = threading.Thread(target=sensor_simulation, args=(sensor_id,))
    t.daemon = True  # Finaliza com o programa principal
    t.start()
    threads.append(t)

# Mantém o script principal rodando
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nEncerrando simulação.")
