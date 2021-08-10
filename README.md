## Description
Instructions for building an indoor air quality measuring device.  
The included NDIR CO2 sensor provides real air concentration readings where most consumer air quality sensors provide estimates.  
This device measures CO2, Particulate Matter, Temperature, and Humidity.  

Where consumer VOC detection devices are error prone, accurate CO2 levels can serve as a useful proxy for clean air.

![Front](img/front.png)
![Back](img/back.png)

## Setup
Make sure Python 3 is installed and run:  
`sudo pip3 install adafruit-circuitpython-scd30`  
This will install the CO2 sensor dependencies  

`pip3 install adafruit-circuitpython-pm25`  
This will install the particulate matter sensor dependencies  

## Run
`cd` into the project directory and run  
`python3 display.py`  

## Run on boot
Configure the renderer to run automatically run when the device boots  
edit `/etc/rc.local`   
add the line `python3 /home/pi/iaq/display.py` at the end of the file, above the `exit 0` line   

It should look something like this: 
```
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

python3 /home/pi/iaq/display.py &

exit 0
```

## Shopping List
https://www.adafruit.com/product/4867 - CO2 Sensor  
https://www.adafruit.com/product/4632 - PM Sensor  
https://www.adafruit.com/product/4210 X2 - QT Cables  
https://www.adafruit.com/product/3934 - eInk display  
https://www.adafruit.com/product/4862 - Display mount and QT connector  
  
If you don't already have a Raspberry Pi:  
https://www.adafruit.com/product/4795 - Device  
https://www.adafruit.com/product/4298 - Power Supply  
https://www.adafruit.com/product/1322 - HDMI Cable  
https://www.adafruit.com/product/4266 - NOOBS SD Card  
