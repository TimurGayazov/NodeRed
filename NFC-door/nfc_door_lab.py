import time
import paho.mqtt.client as mqtt
import sqlite3
db_name = 'door_logs.db'


class DoorLock:
    def __init__(self, mqtt_client):
        self.is_locked = False
        self.mqtt_client = mqtt_client

    def unlock(self):
        self.is_locked = True
        print("Door is unlocked")
        self.mqtt_client.publish("door_status", "unlocked")
        write_to_database('Unlock')

    def lock(self):
        self.is_locked = False
        print("Door is locked")
        self.mqtt_client.publish("door_status", "locked")
        write_to_database('Lock')


def create_database():
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS data(
                    timedate TEXT,
                    state TEXT
                )""")
    connect.commit()


def write_to_database(state):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    mas_data = [time.ctime(), state]
    cursor.execute("INSERT INTO data (timedate, state) VALUES (?, ?)", mas_data)
    connect.commit()


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    create_database()
    client.subscribe("button_press")


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload}")
    if msg.payload == b'press':
        door_lock.unlock()
        time.sleep(10)
        door_lock.lock()


mqtt_client = mqtt.Client()
door_lock = DoorLock(mqtt_client)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("localhost", 1883, 60)

mqtt_client.loop_start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    mqtt_client.disconnect()
    print("Disconnected from MQTT")
