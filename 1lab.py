import paho.mqtt.client as mqtt
import json

# Настройки MQTT брокера
mqtt_broker_address = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "lamp_control_topic"

# Инициализация состояния лампочки
lamp_state = {
    "color": {"r": 0, "g": 0, "b": 0},
    "brightness": 0
}


# Callback-функция, вызываемая при подключении к MQTT брокеру
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Подписываемся на топик для управления лампочкой
    client.subscribe(mqtt_topic)


# Callback-функция, вызываемая при получении нового сообщения из топика
def on_message(client, userdata, msg):
    global lamp_state
    payload = json.loads(msg.payload.decode())

    # Обработка команд для управления лампочкой
    if "color" in payload:
        lamp_state["color"] = payload["color"]
    if "brightness" in payload:
        lamp_state["brightness"] = payload["brightness"]

    # Здесь должен быть ваш код для управления виртуальной лампочкой
    update_lamp(lamp_state)


# Функция для обновления состояния лампочки
def update_lamp(state):
    print("Updating lamp state:", state)
    # Здесь должен быть ваш код для обновления виртуальной лампочки


# Создание MQTT клиента
client = mqtt.Client()

# Назначение callback-функций
client.on_connect = on_connect
client.on_message = on_message

# Подключение к MQTT брокеру
client.connect(mqtt_broker_address, mqtt_broker_port, 60)

# Запуск цикла обработки сообщений
client.loop_forever()
