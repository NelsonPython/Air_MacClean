# CO2-TVOC

<b>You can monitor CO2 and TVOC using a Raspberry Pi and an Adafruit CCS811 gas sensor.</b> TVOC stands for Total Volatile Organic Compounds. This sensor measures CO2 in PPM (parts per million) and TVOCs in PPB (parts per billion).


## <a  href="https://www.adafruit.com/product/3566?gclid=CjwKCAjw4NrpBRBsEiwAUcLcDC7rfEBlaclDQMmAmDsiB-NlT1wL61pWEKSJDLwR02b2QgCL3pEg2RoCNKAQAvD_BwE">CO2-TVOC Sensor<br>
<img src="images/ccs811.png" width=200></a>

## <a href="https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-zero-w">Raspberry Pi Zero W
<img src="images/RasPiZeroHeader.jpg" width=200>
<br>The Raspberry Pi Mega Kit includes a Raspberry Pi Zero W</a> with GPIO header attached plus a 16GB MicroSD memory card with the Raspbian operating system installed.  You can use your own memory card and <a href="https://www.raspberrypi.org/downloads/raspbian/">download and install Raspbian</a> 

## Interacting with Raspberry Pi Zero W

To connect directly to your Raspberry Pi Zero W, you will need a miniHDMI-to-HDMI adaptor and a microUSB-to-USB adaptor.  Power Raspberry Pi with a wall plug or a USB battery capable of powering mobile phones.

You can connect remotely using Secure Shell (SSH).  First, you must enable SSH.  Click the <img src="images/raspberry.png" width=40> raspberry icon on the menu.  Select ```Preferences```, then select ```Raspberry Pi Configuration```.  Click the ```Interfaces``` tab and enable ```SSH```.  

![Window for enabling SSH as described in text](images/SSH.png)


## Building your device

Use this [tutorial](https://learn.adafruit.com/adafruit-ccs811-air-quality-sensor/raspberry-pi-wiring-test) to build your device


## Verifying the version of Python

The Raspbian operating system comes with two versions of Python pre-installed.  This tutorial uses Python 2 and Python 3.  Verify that these versions are installed:

```
python --version
$ Python 2.7.16
```

Verify that Python3 has been pre-installed:

```
python3 --version
$ Python 3.7.3
```

```
pip3 --version
$  pip 18.1 from /usr/lib/python3/dist-packages/pip (python 3.7)
```
## Installing the [PyOTA client library](https://github.com/iotaledger/iota.lib.py)

Install the Pyota client library so you can communicate with the [Tangle](https://docs.iota.org/docs/dev-essentials/0.1/concepts/the-tangle)

>Pyota does not support Python version 3.7.3 as of August 2019. Fortunately, you can still use Python 2.7 for this example.

```
pip install pyota
```

## Installing the [Python IOTA Workshop scripts](https://github.com/iota-community/python-iota-workshop)

This workshop includes a step-by-step tutorial teaching the details of sending and receiving transactions to the Tangle.  They provide the foundation for the code used to store sensor data from EnviroPhat.

Clone the github repository, install the workshop code, and run the "hello world" example.

```
git clone https://github.com/iota-community/python-iota-workshop.git

cd python-iota-workshop
pip install -r requirements.txt
python code/e01_hello_world.py
```

The Tangle will respond with the latest statistics:

```

{u'appName': u'IRI Testnet',
 u'appVersion': u'1.8.0-RC1',
 u'coordinatorAddress': u'EQQFCZBIHRHWPXKMTOLMYUYPCN9XLMJPYZVFJSAY9FQHCCLWTOLLUGKKMXYFDBOOYFBLBI9WUEILGECYM',
 u'duration': 0,
 u'features': [u'dnsRefresher', u'testnet', u'zeroMessageQueue', u'RemotePOW'],
 u'jreAvailableProcessors': 8,
 u'jreFreeMemory': 12670851880L,
 u'jreMaxMemory': 22906667008L,
 u'jreTotalMemory': 16866344960L,
 u'jreVersion': u'1.8.0_181',
 u'lastSnapshottedMilestoneIndex': 1313805,
 u'latestMilestone': TransactionHash('SJWXOHIUGFMOKSSKKFEQJDZDCVOSFSXPAVWDUIUPKUDAJRLVBTPKSHYBAHAFVQAVIHOLKYVSCPCPFE999'),
 u'latestMilestoneIndex': 1313911,
 u'latestSolidSubtangleMilestone': TransactionHash('SJWXOHIUGFMOKSSKKFEQJDZDCVOSFSXPAVWDUIUPKUDAJRLVBTPKSHYBAHAFVQAVIHOLKYVSCPCPFE999'),
 u'latestSolidSubtangleMilestoneIndex': 1313911,
 u'milestoneStartIndex': 434527,
 u'neighbors': 3,
 u'packetsQueueSize': 0,
 u'time': 1565655959126L,
 u'tips': 748,
 u'transactionsToRequest': 0}
```
## Running the CO2-TVOC scripts

Since the CCS811 sensor requires Python 3.7.3 and Pyota requires Python 2.7, I created two scripts:  AQ.py and sendTX.py.  Then, I wrote a shell script to run both python scripts:

```
python3 /home/pi/AQ.py
python /home/pi/sendTX.py
```

I used a cronjob to schedule this shell script to run every 20 minutes.  AQ.py senses the data and saves it to a file.  sendTX.py reads the file and sends the data to the Tangle.

### Sensing data with AQ.py

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
Open the csv file to store the data before sending it to the Tangle
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
### Sending data to the Tangle with sendTX.py

Run using this script immediately after AQ.py.  It reads the last entry from airquality.csv and sends it to the Tangle.  Get started by importing the Iota libraries.
```
from iota import Iota
from iota import ProposedTransaction
from iota import Address
from iota import Tag
from iota import TryteString
from json import load
```
#### sendTX() function
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

## Using your data

You can store sensor directly to the Tangle and view it using the Tangle Explorer.  You can use custom scripts or the ZMQ listener to retrieve it.

[Storing sensor data on the Tangle](co2-direct2Tangle.md)

[Viewing data using the Devnet Tangle Explorer](https://devnet.thetangle.org/)

[Retrieving data]()

[Retrieving data using ZMQ](zmq_listener.md)

## Selling your data

You sell data by publishing it on the I3 Consortium Data Marketplace where subscribers can buy it:

[Publishing data to the I3 Data Marketplace](co2-I3-publish.md)

[Retrieving your data subscription](co2-I3-subscribe.md)


## Investigating patterns in your data

Plotting CO2 and TVOC data over time shows how air quality may change.  Use this data science notebook to get started [investigating patterns in CO2-TVOC data](https://www.kaggle.com/nelsondata/los-angeles-air-quality)

## Planning for the future

- When Pyota supports Python 3.7.3, update AQ.py to send data to the Tangle without saving it to a file

