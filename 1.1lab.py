import tkinter as tk
from tkinter import Canvas
import json
import paho.mqtt.client as mqtt

mqtt_broker_address = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "lamp_control_topic"

lamp_state = {
    "color": {"r": 0, "g": 0, "b": 0},
    "brightness": 0
}


def update_lamp(state):
    brightness_percentage = state["brightness"]
    alpha = brightness_percentage / 100.0  # Преобразование яркости в диапазон от 0.0 до 1.0
    adjusted_color = {
        "r": int(state["color"]["r"] * alpha),
        "g": int(state["color"]["g"] * alpha),
        "b": int(state["color"]["b"] * alpha)
    }

    canvas.itemconfig(lamp, fill=f'#{adjusted_color["r"]:02X}{adjusted_color["g"]:02X}{adjusted_color["b"]:02X}')
    canvas.itemconfig(brightness_text, text=f'Brightness: {brightness_percentage}%')
    print("Lamp state updated:", state)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)


def on_message(client, userdata, msg):
    global lamp_state
    payload = json.loads(msg.payload.decode())
    if "color" in payload:
        lamp_state["color"] = payload["color"]
    if "brightness" in payload:
        lamp_state["brightness"] = payload["brightness"]
    update_lamp(lamp_state)


def create_lamp_window():
    window = tk.Tk()
    window.title("Smart Lamp")

    global canvas
    canvas = Canvas(window, width=200, height=200, bg="white")
    global lamp
    lamp = canvas.create_oval(50, 50, 150, 150, fill="#000000")
    canvas.pack()

    global brightness_text
    brightness_text = canvas.create_text(100, 180, text="Brightness: 0%", font=("Helvetica", 10))

    return window


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_address, mqtt_broker_port, 60)

lamp_window = create_lamp_window()

client.loop_start()
lamp_window.mainloop()
