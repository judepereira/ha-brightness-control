# ha-brightness-control
A simple Python app to expose your Raspberry Pi's DSI display brightness 
to Home Assistant via MQTT discoverable.

This app was heavily adapted using the light demo 
[here](https://github.com/unixorn/ha-mqtt-discoverable?tab=readme-ov-file#usage-6).

## Origin Story
My use case was to control the backlight on my DIY photo frame, 
powered by a 10.1 inch DSI display connected to a Raspberry Pi.

## Usage
Controlling the brightness of a DSI display is usually by writing the
desired brightness value to a specific file. In my case, it was `/sys/class/backlight/10-0045/brightness`. 
```shell
# git clone this repo
$ cd ha-brightness-control
$ python3.11 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ export MQTT_HOST=<your HA MQTT host>
$ export BACKLIGHT_CONTROL_FILE=/sys/class/backlight/10-0045/brightness 
# You might need to run the following as root
$ python main.py
```
