import paho.mqtt.publish as publish
import json

mqtt_broker_address = "localhost"
mqtt_topic = "lamp_control_topic"

# Сообщение для отправки
message = {
    "color": {"r": 0, "g": 0, "b": 255},
    "brightness": 100
}

# Опубликовать сообщение
publish.single(mqtt_topic, payload=json.dumps(message), hostname=mqtt_broker_address)
