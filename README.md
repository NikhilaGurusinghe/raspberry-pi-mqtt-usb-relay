# How to run
Must use paho-mqtt pip package
```pip3 install paho-mqtt```

Uses [uhubctl](https://github.com/mvp/uhubctl) to control the Raspberry Pi's usb ports
```sudo apt install uhubctl```

The command sent to disable a Raspberry Pi 3B's ports is:
```sudo uhubctl -l 1-1 -p 2 -a off```
Where "off" can either be "off" or "on".