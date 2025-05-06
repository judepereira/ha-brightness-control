import json
import os
import socket
import sys
import time
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import Light, LightInfo
from paho.mqtt.client import Client, MQTTMessage

mqtt_host = os.getenv("MQTT_HOST")
bl_file = os.getenv("BACKLIGHT_CONTROL_FILE")
device_name = os.getenv("DEVICE_NAME", socket.gethostname())

if not mqtt_host:
    sys.stderr.write("No MQTT host found! Set MQTT_HOST")
    sys.exit(1)

if not bl_file:
    sys.stderr.write("No backlight control file found! Set BACKLIGHT_CONTROL_FILE")
    sys.exit(1)

mqtt_settings = Settings.MQTT(host=mqtt_host)

light_info = LightInfo(
    name=f"{device_name} Backlight",
    unique_id=f"backlight_control_{device_name}",
    brightness=True,
    effect=False)

settings = Settings(mqtt=mqtt_settings, entity=light_info)

with open(bl_file, 'r') as f:
    last_brightness = int(f.readline())


def write_brightness(level: int):
    bl.brightness(level)
    if level == 0:
        bl.off()
    else:
        bl.on()

    with open(bl_file, "w") as f:
        f.write(f"{level}")


def my_callback(client: Client, user_data, message: MQTTMessage):
    global last_brightness
    try:
        payload = json.loads(message.payload.decode())
    except ValueError as error:
        print("Ony JSON schema is supported for light entities!")
        return

    print(f'Received: f{payload}')

    if "brightness" in payload:
        brightness = payload["brightness"]
        write_brightness(int(brightness))
        last_brightness = brightness
    elif "state" in payload:
        if payload["state"] == light_info.payload_on:
            write_brightness(last_brightness)
        else:
            write_brightness(0)


bl = Light(settings, my_callback, None)

write_brightness(last_brightness)

print("Press Ctrl + C to quit...")
while True:
    try:
        time.sleep(60)
    except KeyboardInterrupt:
        break
