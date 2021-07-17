# Shared libraries

import time
import board
import busio

# Display initialization
from inky.auto import auto
inky_display = auto()
inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw



# Display font

from font_fredoka_one import FredokaOne

font = ImageFont.truetype(FredokaOne, 22)

# PM Sensor initialization

from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C


reset_pin = None

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
pm25 = PM25_I2C(i2c, reset_pin)

# CO2 Sensor initialization

import adafruit_scd30

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)
# scd.temperature_offset = 10
print("Temperature offset:", scd.temperature_offset)

# scd.measurement_interval = 4
print("Measurement interval:", scd.measurement_interval)

# scd.self_calibration_enabled = True
print("Self-calibration enabled:", scd.self_calibration_enabled)

# scd.ambient_pressure = 1100
print("Ambient Pressure:", scd.ambient_pressure)

# scd.altitude = 100
print("Altitude:", scd.altitude, "meters above sea level")

# scd.forced_recalibration_reference = 409
print("Forced recalibration reference:", scd.forced_recalibration_reference)
print("")

while True:

    # Get PM Data
    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue
    
    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

    # Get Sensirion data
    data = scd.data_available
    if data:
        print("Data Available!")
        print("CO2:", scd.CO2, "PPM")
        print("Temperature:", scd.temperature, "degrees C")
        print("Humidity::", scd.relative_humidity, "%%rH")
        hum = scd.relative_humidity
        print("")
        print("Waiting for new data...")
        print("")
        
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)
                
        message = ("CO2: " + str(scd.CO2)[0:7] + " PPM\n" +
        "Temp: " + str((scd.temperature * 1.8) + 32)[0:6] + "\n" +
                   "Humidity: " + str(hum)[0:5] + "\n" +
                   "PM: 0.3|0.5|1.0|2.5|5.0|10\n" +
                   "       " + str(aqdata["particles 03um"]) +
                   " |" + str(aqdata["particles 05um"]) +
                   " |" + str(aqdata["particles 10um"]) +
                   " |" + str(aqdata["particles 25um"]) +
                   " |" + str(aqdata["particles 50um"]) +
                   " |" + str(aqdata["particles 100um"])
                   )
        
        
        w, h = font.getsize(message)
        x = (inky_display.WIDTH / 2) - (w / 2)
        y = (inky_display.HEIGHT / 2) - (h / 2)

        draw.text((-1, -5), message, inky_display.BLACK, font)
        inky_display.set_image(img)
        inky_display.show()

    time.sleep(15)
