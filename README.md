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

## Installing the [Python IOTA Workshop scripts](https://github.com/iota-community/python-iota-workshop)

This will install the Pyota client library so you can communicate with the [Tangle](https://docs.iota.org/docs/dev-essentials/0.1/concepts/the-tangle).  This workshop includes a step-by-step tutorial teaching the details of sending and receiving transactions to the Tangle.  They provide the foundation for the code used to store sensor data from CO2-TVOC.

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

## Using your data

You can store sensor directly to the Tangle and view it using the Tangle Explorer.  You can use custom scripts or the ZMQ listener to retrieve it.

[Storing sensor data on the Tangle](co2-direct2Tangle.md)

[Viewing data using the Devnet Tangle Explorer](https://devnet.thetangle.org/)

[Retrieving data]()

[Retrieving data using ZMQ](https://github.com/NelsonPython/IoT-ZMQ-listener/blob/master/README.md)

## Selling your data

You sell data by publishing it on the I3 Consortium Data Marketplace where subscribers can buy it:

[Publishing data to the I3 Data Marketplace](co2-I3-publish.md)

[Retrieving your data subscription](co2-I3-subscribe.md)


## Investigating patterns in your data

Plotting CO2 and TVOC data over time shows how air quality may change.  Use this data science notebook to get started [investigating patterns in CO2-TVOC data](https://www.kaggle.com/nelsondata/los-angeles-air-quality)

## Planning for the future

- When Pyota supports Python 3.7.3, update AQ.py to send data to the Tangle without saving it to a file
