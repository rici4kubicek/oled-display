# OLED Displej SSD1306

import time, json
from datetime import datetime
from pytz import timezone
import Adafruit_SSD1306
import paho.mqtt.client as mqtt

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

mqtt_ready = 0
text_to_show = {}
text_to_show["text"] = ""
text_to_show["timeout"] = 0
temp_time = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus='0')
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# create object
draw = ImageDraw.Draw(image)

# clear display
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0

# load basic font
#font = ImageFont.load_default()
font = ImageFont.truetype('Vafle_VUT_Regular.ttf', 10)


def on_show(moqs, obj, msg):
    global text_to_show, temp_time
    try:
        text_to_show = json.loads(msg.payload.decode('utf-8'))["text"]
        temp_time =  json.loads(msg.payload.decode('utf-8'))["timeout"]
    except:
        pass


def on_disconnect(client, userdata, rc):
    global mqtt_ready
    mqtt_ready = 0
    retry_time = 2
    while rc != 0:
        time.sleep(retry_time)
        try:
            rc = mqttc.reconnect()
        except Exception as e:
            rc = 1
            retry_time = 2  # probably wifi/internet problem so slow down the reconnect periode


def on_connect(mqtt_client, obj, flags, rc):
    global mqtt_ready
    mqtt_ready = 1
    mqttc.subscribe('display/#')


if __name__ == "__main__":

    mqttc = mqtt.Client()

    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.message_callback_add('display/show', on_show)

    try:
        mqttc.connect("localhost", 1883, 30)
        mqtt_ready = 1
        time.sleep(3)  # small timeout to catch thread errors to MQTT
    except Exception:
        mqtt_ready = 0

    mqttc.loop_start()

    cnt = 0
    temp_time = 0

    while True:

        # clear display
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True )

        now_utc = datetime.now(timezone('UTC'))
        now_local = now_utc.astimezone(timezone('Europe/Prague'))

        if cnt < 5:
            draw.text((x, top + 2), "Sku rAAS module", font=font, fill=255)
        else:
            if temp_time > 0:
                draw.text((x, top + 2), text_to_show, font=font, fill=255)
            else:
                draw.text((x, top + 2), "", font=font, fill=255)

        draw.text((x, top + 12), "IP: " + str(IP)[2:-3],  font=font, fill=255)
        draw.text((x, top + 22), now_local.strftime("%H:%M:%S %d.%m.%Y"), font=font, fill=255)

        # display it
        disp.image(image)
        disp.display()
        cnt = cnt + 1

        if temp_time > 0:
            temp_time = temp_time - 1

        time.sleep(1)