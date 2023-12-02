from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import paho.mqtt.client as mqtt

class DoorLockApp(App):
    def build(self):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.connect("localhost", 1883, 60)  # Замените настройки вашего MQTT-брокера
        self.mqtt_client.loop_start()

        layout = BoxLayout(orientation='vertical', padding=10)
        button = Button(text='Unlock Door')
        button.bind(on_press=self.unlock_door)
        layout.add_widget(button)

        return layout

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("door_status")

    def unlock_door(self, instance):
        self.mqtt_client.publish("button_press", "press")


if __name__ == '__main__':
    DoorLockApp().run()
