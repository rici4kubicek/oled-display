# OLED Displej SSD1306

# pripojeni knihoven
import time
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Nastaveni displeje 128x64 s hardware I2C sbernici
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus='0')

# Zahajeni komunikace s displejem
disp.begin()

# Vycisteni displeje
disp.clear()
disp.display()

# Vytvoreni prazdneho obrazce pro vymazani displeje
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Vytvoreni objektu pro kresleni
draw = ImageDraw.Draw(image)

# Vykresleni cerneho obdelnika pro vymazani obsahu displeje
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Konstanty pro jednoduche kresleni
padding = -2
top = padding
bottom = height-padding
x = 0

# Nacteni zakladniho pisma
font = ImageFont.load_default()

# Muzeme pouzit take jine fonty, napriklad z:
# http://www.dafont.com/bitmap.php
# Pote staci umistit font do stejne slozky a nastavit:
# font = ImageFont.truetype('RetroComputer.ttf', 8)

while True:

    # Vykresleni cerneho obdelnika pro vymazani obrazovky
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )

    now_utc = datetime.now(timezone('UTC'))
    now_local = now_utc.astimezone(timezone('Europe/Prague'))

    draw.text((x, top), "Sku rAAS module", font=font, fill=255)

    draw.text((x, top + 9), "IP: " + str(IP)[2:-3],  font=font, fill=255)
    draw.text((x, top + 17), now_local.strftime("%H:%M:%S %d.%m.%Y"), font=font, fill=255)


    # Zobrazeni na displej
    disp.image(image)
    disp.display()
    # Kratka pauza 100 ms
    time.sleep(5)