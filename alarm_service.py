import tkinter as tk
from paho.mqtt.client import Client
from datetime import datetime

MAX_NOTIFICATIONS = 30  # Máximo de notificações visíveis

def on_connect(client, userdata, flags, rc):
    client.subscribe("events/#")

def on_message(client, userdata, msg):
    now = datetime.now().strftime("%H:%M:%S")

    if msg.topic == "events/high_temperature":
        message = f"[{now}] 🔥 Temperatura alta detectada!"
    elif msg.topic == "events/sudden_change":
        message = f"[{now}] ⚠️ Mudança brusca de temperatura!"
    else:
        return

    # Atualiza a lista de alertas no topo
    alert_list.insert(0, message)

    # Emite som de alerta
    app.bell()

    # Limita a quantidade de mensagens
    if alert_list.size() > MAX_NOTIFICATIONS:
        alert_list.delete(tk.END)

# Interface gráfica
app = tk.Tk()
app.title("Monitor de Alarmes")
app.geometry("400x600")

alert_list = tk.Listbox(app, height=MAX_NOTIFICATIONS, font=("Segoe UI", 11))
alert_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Cliente MQTT
client = Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_start()

app.mainloop()
