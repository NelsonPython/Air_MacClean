import time
import datetime
import sys
import board
import busio
import adafruit_ccs811
from statistics import mean
import getIP
import textStatus

acIP = getIP.getIP()
print(acIP)
textStatus.textStatus(acIP)

i2c_bus = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c_bus)

fo = open("/home/pi/airquality.csv","a")

co2 = []
tvoc = []

for k in range(20):
    try:
      if not ccs811.data_ready:
          pass
      else:
          if ccs811.eco2 > 0:
              co2.append(ccs811.eco2)
              tvoc.append(ccs811.tvoc)
              print("C02 %1.0f PPM" % ccs811.eco2, end=" ")
              print("TVOC %1.0f PPB" % ccs811.tvoc)
          else:
              print("eco2=0")

    except KeyboardInterrupt:
        fo.close()
        sys.exit()
    time.sleep(3)

avgCO2 = mean(co2)
avgTVOC = mean(tvoc)
timestamp = datetime.datetime.now()
timestamp = timestamp.strftime("%Y-%m-%d %H:%M")
msg=str(round(avgCO2,0))+","+str(round(avgTVOC,0))+","+str(timestamp)
print(msg)
textStatus.textStatus(msg)
print(msg, file=fo)
fo.close()
