<h1>Viewing air quality data</h1>

<b>Air MacClean senses CO2 and TVOC</b>

testccs811.py senses air quality data

```
import time
import board
import busio
import adafruit_ccs811

i2c_bus = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c_bus)

while True:

    if not ccs811.data_ready:
        pass
    else:
        print("CO2: %1.0f PPM" % ccs811.eco2)
        print("TVOC: %1.0f PPB" % ccs811.tvoc)
    time.sleep(5)
```

Sample sensor data

```
pi@raspberrypi:~/AirQuality $ python3 testccs811.py
CO2: 407 PPM
TVOC: 1 PPM
```
