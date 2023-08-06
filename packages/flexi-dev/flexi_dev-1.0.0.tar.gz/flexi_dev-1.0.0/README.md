# flexi_dev

## Flexible Input Devices

Extend your applications/scripts by using events from an input device to trigger actions.

Do you have a spare bluetooth mouse that you wish you could use as a remote control for triggering actions on your raspberry pi?

do you have repetitive strain injury (RSI) in your hands and wish that you could use an old keyboard as an input device to trigger actions using your feet?


## Install

```sh
$ pip install flexi_dev
```


## Prerequisites

Your user needs to be able to read from the chosen input device.

Find out device permissions:

```sh
$ ls -l /dev/input
total 0
drwxr-xr-x 2 root root     200 Feb 19 07:41 by-id
drwxr-xr-x 2 root root     280 Feb 19 07:41 by-path
crw-rw---- 1 root input 13, 64 Feb 17 16:00 event0
crw-rw---- 1 root input 13, 65 Feb 17 16:00 event1
crw-rw---- 1 root input 13, 66 Feb 17 16:00 event2
.......... . .... ..... ... .. ... .. ..... ......
.......... . .... ..... ... .. ... .. ..... ......    
crw-rw---- 1 root input 13, 73 Feb 17 16:00 event9
.......... . .... ..... ... .. ... .. ..... ......
crw-rw---- 1 root input 13, 34 Feb 17 16:00 mouse2
$
```

verify that the local user belong to the input group:

```sh
$ groups
adm cdrom sudo audio dip plugdev input lpadmin lxd sambashare davfs2
$
```

List the current input devices recognized by Xorg:

```sh
$ xinput list > /tmp/old
```

Plug in your mouse and relist:

```sh
$ xinput list > /tmp/new
```

```sh
$ diff -u /tmp/old /tmp/new
--- /tmp/old	2022-02-19 14:01:19.802425450 +0000
+++ /tmp/new	2022-02-19 14:01:43.510674690 +0000
@@ -3,6 +3,7 @@
 ⎜   ↳ EST Gaming keyboard                     	id=9	[slave  pointer  (2)]
+⎜   ↳ Lenovo Ultraslim Plus Wireless Keyboard & Mouse	id=14	[slave  pointer  (2)]
 ⎣ Virtual core keyboard                   	id=3	[master keyboard (2)]
```

Note the *id*.
We don't want our mouse to move the normal mouse pointer or to perform any normal button presses so we need to disable it:
 
```sh
$ xinput set-int-prop $id "Device Enabled" 8 0
```

The input device is now ours to play with.

## Simple Example

Now use our prepared device to print something to the terminal when we left/right click:

 
```python
#!/usr/bin/env python3
import logging
import sys
import trio
from flexi_dev.MouseDriver import MouseDriver

class MickeyMouse(MouseDriver):
    def __init__(self, device, *args, **kwargs):
        super(MickeyMouse, self).__init__(device=device, *args, **kwargs)

    async def ms_btn9(self, **kwargs):
        print("left button pressed")

    async def ms_btn10(self, **kwargs):
        print("right button pressed, quitting...")
        sys.exit() 

logger = logging.getLogger('flexi_dev')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('flexi_dev.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

m = MickeyMouse('/dev/input/by-id/usb-17ef_Lenovo_Ultraslim_Plus_Wireless_Keyboard___Mouse-if01-mouse')
trio.run(m.run)
```
