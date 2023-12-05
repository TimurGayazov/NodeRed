import time
import paho.mqtt.client as mqtt
import sqlite3
import threading
db_name = 'door_logs.db'


class DoorLock:
    def __init__(self, mqtt_client):
        self.is_locked = False
        self.mqtt_client = mqtt_client

    def unlock(self):
        self.is_locked = True
        print("Door is unlocked")
        self.mqtt_client.publish("door_status", "unlock")
        self.mqtt_client.publish("onoff", "false")
        write_to_database('Unlock')

    def lock(self):
        self.is_locked = False
        print("Door is locked")
        self.mqtt_client.publish("door_status", "lock")
        self.mqtt_client.publish("onoff", "true")
        write_to_database('Lock')

    def auto_mode(self):
        self.is_locked = True
        print("Door is unlocked")
        self.mqtt_client.publish("door_status", "unlock")
        self.mqtt_client.publish("onoff", "false")
        write_to_database('Unlock')

        threading.Timer(5, self.complete_auto_mode).start()

    def complete_auto_mode(self):
        self.is_locked = False
        print("Door is locked")
        self.mqtt_client.publish("door_status", "lock")
        self.mqtt_client.publish("onoff", "true")
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
    print(f'{state} было записано в базу данных')

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    create_database()
    client.subscribe("button_press")


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload}")
    if msg.payload == b'unlock':
        door_lock.unlock()
    elif msg.payload == b'lock':
        door_lock.lock()
    elif msg.payload == b'auto-mode':
        door_lock.auto_mode()


mqtt_client = mqtt.Client()
door_lock = DoorLock(mqtt_client)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("10.3.3.216", 1883, 60)

mqtt_client.loop_start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    mqtt_client.disconnect()
    print("Disconnected from MQTT")
