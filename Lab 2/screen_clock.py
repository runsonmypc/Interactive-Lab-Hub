import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    # Draw a black filled box to clear the image.
    #image = Image.new("RGB", (width, height))
    draw.rectangle((0, 0, width, height), outline=0, fill="#0000FF")

    #Todo: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py
    second = float(time.strftime("%S"))
    minute = float(time.strftime("%M"))
    hour = float(time.strftime("%H"))

    secwidth = (second/60) * width
    minwidth = (minute/60) * width
    hourwidth = (hour/24) * width

    current_time = time.strftime("Date: "+"%m/%d/%Y\n")
    current_date = time.strftime("Time: "+"%H:%M")
    y = top

    if buttonA.value and buttonB.value:
        draw.rectangle((0, 0, secwidth, height), outline = 0, fill = "#FFA500")
    else:
        backlight.value = True  # turn on backlight

    if buttonB.value and not buttonA.value:  # just button A pressed
        draw.rectangle((0, 0, minwidth, height), outline = 0, fill = "#00FF00")
        draw.text((x, y), "Minute", font=font, fill="#000000")

    if buttonA.value and not buttonB.value:  # just button B pressed
        draw.rectangle((0, 0, hourwidth, height), outline = 0, fill = "#FF0000")
        draw.text((x, y), "Hour", font=font, fill="#000000")  # date

    if not buttonA.value and not buttonB.value:  # both pressed
        image = Image.open("Rickroll.jpg")
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
            image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))


    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
