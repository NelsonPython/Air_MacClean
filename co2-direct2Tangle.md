# Storing sensor data on the Tangle

Since the CCS811 sensor requires Python 3.7.3 and Pyota requires Python 2.7, I created two scripts:  [AQ.py](https://github.com/NelsonPython/CO2TVOC/blob/master/code/AQ.py) and [sendTX.py](https://github.com/NelsonPython/CO2TVOC/blob/master/code/sendTX.py).  Then, I wrote a shell script to run them:

```
python3 /home/pi/AQ.py
python /home/pi/sendTX.py
```

I used cron to schedule this shell script to run every 20 minutes.  AQ.py senses the data and saves it to a file.  sendTX.py reads the last line of the file and sends the data to the Tangle.

## Sensing data with AQ.py

In order for sensor data to be meaningful, you must record the time the sensor reading was taken.  Import time and datetime libraries.  

```
import time
import datetime
```
Import the system and the sensor libraries

```
import sys
import board
import busio
import adafruit_ccs811
```
The sensor has a brief start up period before it begins sensing data.  To account for this, it takes 20 readings then computes the average.  So the statistics package is imported for that computation.
```
from statistics import mean
```
In order to run this sensor without a monitor, you must know it's network address.  Import the getIP.py script.
```
import getIP
```
In order to text the IP address and the sensor data, import textStatus.py
```
import textStatus
```
When the device starts it gets the IP address and sends a text
```
acIP = getIP.getIP()
print(acIP)
textStatus.textStatus(acIP)
```
Setup the i2c bus and instantiate the sensor
```
i2c_bus = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c_bus)
```
Open the csv file to store the data
```
fo = open("/home/pi/airquality.csv","a")
```
Take 20 sensor readings then compute the average
```
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
```
Format the data to be stored
```
avgCO2 = mean(co2)
avgTVOC = mean(tvoc)
timestamp = datetime.datetime.now()
timestamp = timestamp.strftime("%Y-%m-%d %H:%M")
msg=str(round(avgCO2,0))+","+str(round(avgTVOC,0))+","+str(timestamp)
print(msg)
```
Text the data and store it
```
textStatus.textStatus(msg)
print(msg, file=fo)
fo.close()
```
## Sending data to the Tangle with sendTX.py

Run using this script immediately after AQ.py.  It reads the last entry from airquality.csv and sends it to the Tangle.  Get started by importing the Iota libraries.
```
from iota import Iota
from iota import ProposedTransaction
from iota import Address
from iota import Tag
from iota import TryteString
from json import load
```
### sendTX() function
```
def sendTX(msg):
    '''
    PURPOSE:  send transaction to the Tangle

    INPUT:
    seed
    address from a different seed

    OUTPUT:
    sends a data transaction to the IOTA testbed
    '''
```
In order to send a transaction to the Tangle, you need an 81-tryte seed and one address from a different seed.  Use /python-iota-workshop/code/e04_generate_address.py to generate the address.  

```
def sendTX(msg):
        seed =    'SEED99999999999999999999999999999999999999999999999999999999999999999999999999999'
        address = 'ADDRESS99999999999999999999999999999999999999999999999999999999999999999999999999'
```
### Setting the testbed

For purposes of testing, connect to the IOTA testbed, called "Devnet"

```
        api = Iota('https://nodes.devnet.iota.org:443',seed)
```
### Sending the data transaction

An IOTA data transaction includes the address, message, tag, and a value of zero.  The message must be converted to a TryteString.  The tag must be of type "Tag".  Data transactions always have a value of zero.

```
        tx = ProposedTransaction(
                address=Address(address),
                message=TryteString.from_unicode(msg),
                tag=Tag('LACOTVOC'),
                value=0
        )
```
There are two steps to sending a transaction:  preparing the transaction and sending the trytes.  In this example, an exception is raised if the transaction cannot be properly prepared.  However, an exception is not raised, if the transaction cannot be sent.

```
        try:
                tx=api.prepare_transfer(transfers=[tx])
        except Exception as e:
                print("Check prepare_transfer ", e)
                raise
        try:
                result=api.send_trytes(tx['trytes'],
                depth=3,min_weight_magnitude=9)
        except:
                print("Check send_trytes")
```
First, open the airquality.csv file.  Read the last line. Strip the special characters "\n".  Send the data then close the file.

```
if __name__=="__main__":
        f = open("airquality.csv","r")
        msg = f.readlines()[-1]
        msg = msg.strip("\n")
        print(msg)
        try:
            sendTX(msg)
        except e:
            print("Check devnet",e)
        f.close()
```
