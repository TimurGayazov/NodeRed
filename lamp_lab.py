import time
import tkinter as tk
import paho.mqtt.client as mqtt
import sqlite3

db_name = 'logs.db'


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def create_database():
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS data(
                    timedate TEXT,
                    topic TEXT,
                    payload TEXT
                )""")
    connect.commit()


def write_to_database(topic, payload):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    mas_data = [time.ctime(), topic, payload]
    cursor.execute("INSERT INTO data (timedate, topic, payload) VALUES (?, ?, ?)", mas_data)

    connect.commit()


def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print(f"Received message on topic {message.topic}: {payload}")
    topic = message.topic
    write_to_database(topic, payload)
    if message.topic == "lamp/brightness":
        brightness_scale.set(int(payload))
    elif message.topic == "lamp/rgb":
        rgb = hex_to_rgb(payload)
        color_entry_r.delete(0, tk.END)
        color_entry_r.insert(0, str(int(rgb[0])))

        color_entry_g.delete(0, tk.END)
        color_entry_g.insert(0, str(int(rgb[1])))

        color_entry_b.delete(0, tk.END)
        color_entry_b.insert(0, str(int(rgb[2])))

        color_hex = rgb_to_hex(rgb)
        lamp_canvas.delete("lamp_circle")
        lamp_canvas.create_oval(50, 50, 150, 150, fill=color_hex, outline='#000000', tags="lamp_circle")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    create_database()
    client.subscribe("lamp/+")


def send_command(color_r, color_g, color_b, brightness):
    client.publish("lamp/rgb", rgb_to_hex((color_r, color_g, color_b)))
    client.publish("lamp/brightness", brightness)


def update_lamp():
    color_r = color_entry_r.get()
    color_g = color_entry_g.get()
    color_b = color_entry_b.get()
    brightness = brightness_scale.get()
    send_command(color_r, color_g, color_b, brightness)


root = tk.Tk()
root.title("Lamp")
root.configure(bg='#2E2E2E')  # Set dark background color

lamp_canvas = tk.Canvas(root, width=200, height=200, bg='#2E2E2E')
lamp_canvas.pack()

color_label = tk.Label(root, bg='#2E2E2E', fg='white')
color_label.pack()

color_entry_r = tk.Entry(root, width=5)
color_entry_r.pack(side=tk.LEFT, padx=5)

color_entry_g = tk.Entry(root, width=5)
color_entry_g.pack(side=tk.LEFT, padx=5)

color_entry_b = tk.Entry(root, width=5)
color_entry_b.pack(side=tk.LEFT, padx=5)

brightness_label = tk.Label(root, text="Brightness:", bg='#2E2E2E', fg='white')
brightness_label.pack(pady=5)

brightness_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
brightness_scale.pack(pady=5)

update_button = tk.Button(root, text="Update Lamp", command=update_lamp, bg='#282828', fg='white', font=("Arial", 12))
update_button.pack(pady=10, side=tk.TOP, anchor=tk.CENTER)  # Center the button

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.loop_start()

root.mainloop()
