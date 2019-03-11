# OLED Displej SSD1306

# pripojeni knihoven
import time
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

    # Skripty pro nacteni informaci o systemu, zdroj:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )

    # Vypsani nactenych udaju na souradnice x, top s danym fontem a barvou (fill)

    draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
    draw.text((x, top+8),     str(CPU), font=font, fill=255)
    draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
    draw.text((x, top+25),    str(Disk),  font=font, fill=255)
    # Vypsani naseho textu
    draw.text((x, top+32),    str("Arduino navody"),  font=font, fill=127)

    # Zobrazeni na displej
    disp.image(image)
    disp.display()
    # Kratka pauza 100 ms
    time.sleep(5)