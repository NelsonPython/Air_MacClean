# Air MacClean

<b>You can monitor CO2 and TVOC using a Raspberry Pi and an Adafruit CCS811 gas sensor.</b> TVOC stands for Total Volatile Organic Compounds. This sensor measures CO2 in PPM (parts per million) and TVOCs in PPB (parts per billion).


## <a  href="https://www.adafruit.com/product/3566?gclid=CjwKCAjw4NrpBRBsEiwAUcLcDC7rfEBlaclDQMmAmDsiB-NlT1wL61pWEKSJDLwR02b2QgCL3pEg2RoCNKAQAvD_BwE">CO2-TVOC Sensor<br>
<img src="images/ccs811.png" width=200></a>

## <a href="https://thepihut.com/collections/raspberry-pi/products/raspberry-pi-zero-w">Raspberry Pi Zero W
<img src="images/RasPiZeroHeader.jpg" width=200>
<br>The Raspberry Pi Mega Kit includes a Raspberry Pi Zero W</a> with GPIO header attached plus a 16GB MicroSD memory card with the Raspbian operating system installed.  You can use your own memory card and <a href="https://www.raspberrypi.org/downloads/raspbian/">download and install Raspbian</a> 

## Interacting with Raspberry Pi Zero W

Use a miniHDMI-to-HDMI adaptor to connect Enviro to a monitor or TV.  Use a microUSB-to-USB adaptor to plug-in a keyboard or mouse.  I recommend a [USB hub](https://www.bestbuy.com/site/insignia-4-port-usb-3-0-hub-black/4333600.p?skuId=4333600&ref=212&loc=1&ref=212&loc=1&gclid=EAIaIQobChMI0_6gr9_P6QIVT-zjBx3WpAuAEAQYBCABEgKemvD_BwE&gclsrc=aw.ds) so you can connect both of them.  Power Raspberry Pi with a wall plug or a USB battery capable of powering mobile phones.

You can connect remotely using Secure Shell (SSH) but you must enable SSH.  Click the <img src="images/raspberry.png" width=40> raspberry icon on the menu.  Select ```Preferences```, then select ```Raspberry Pi Configuration```.  Click the ```Interfaces``` tab and enable ```SSH```.  

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

## Gathering data

stay tuned...

## Investigating your data

What happens when you plot air quality data over time.  Use this data science notebook to explore [investigating CO2-TVOC data](https://www.kaggle.com/nelsondata/los-angeles-air-quality)

[Charting CO2 data on ThingSpeak](https://thingspeak.com/channels/865249)

## Known bugs

- As of October 2019, Raspberry Pi Buster operating system may have a WiFi Bug:  https://www.raspberrypi.org/forums/viewtopic.php?t=252984. 
