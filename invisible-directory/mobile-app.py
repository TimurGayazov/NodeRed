import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("door_status")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload}")
    if msg.payload == b'unlocked':
        messagebox.showinfo("Door Unlocked", "The door is now unlocked!")

def unlock_door():
    mqtt_client.publish("button_press", "press")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("localhost", 1883, 60)  # Замените настройки вашего MQTT-брокера
mqtt_client.loop_start()

app = tk.Tk()
app.title("Door Lock App")

button = tk.Button(app, text="Unlock Door", command=unlock_door)
button.pack(pady=20)

app.mainloop()
