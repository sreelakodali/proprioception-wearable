	# Reading and Saving Serial Data from MCU
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial
import datetime
import csv
import os
import numpy as np
from scipy import signal
import asyncio
from bleak import BleakScanner, BleakClient
import time
import sys
from itertools import count, takewhile
from typing import Iterator
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData




#addr_Adafruit1 = "026B8104-5A8F-E8AF-518E-B778DB1C9CE2"
addr_BLE1 = "D4:D6:30:F2:D0:88:CD:AC"
UART_SERVICE_UUID_BLE1 = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID_BLE1 = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" # 2, RX write
UART_TX_CHAR_UUID_BLE1 = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" # 3, TX notify
name = "Adafruit Bluefruit LE"


async def quickScan():
    devices = await BleakScanner.discover()
    #print(len(devices))
    for dev in devices:
        # if (dev.name == name):
        print(dev.name)

# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))

async def main():
    device = await BleakScanner.find_device_by_address(addr_BLE1)
    #device = await BleakScanner.find_device_by_name(name)
    if device is None:
        print("could not find device with name {}".format(name))
    else:
        print(device)

        def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
            print("received:", data)

        async with BleakClient(device.address) as client:
            print("Connected! MTU size = {}".format(client.mtu_size))

            await client.start_notify(UART_TX_CHAR_UUID_BLE1, handle_rx)
            loop = asyncio.get_running_loop()
            nus = client.services.get_service(UART_SERVICE_UUID_BLE1)
            rx_char = nus.get_characteristic(UART_RX_CHAR_UUID_BLE1)         

            while True:
                await asyncio.sleep(0.01)
                  #data = input()
                  #print("Sending: " + str(data))
                  #data = data.encode(encoding="ascii")
                  #await client.write_gatt_char(rx_char, data, response=False)
            #     # This waits until you type a line and press ENTER.
            #     # A real terminal program might put stdin in raw mode so that things
            #     # like CTRL+C get passed to the remote device.

                data = await loop.run_in_executor(None, sys.stdin.buffer.readline)

            # # data will be empty on EOF (e.g. CTRL+D on *nix)
                if not data:
                    break

            #     # Writing without response requires that the data can fit in a
            #     # single BLE packet. We can use the max_write_without_response_size
            #     # property to split the data into chunks that will fit.
            #     #data = data.rstrip()
                for s in sliced(data, rx_char.max_write_without_response_size):
                    print(s)
                    await client.write_gatt_char(rx_char, s)

                print("sent:", data)

            # for char in nus.characteristics:
            #     print(char)

asyncio.run(main())



# ## CONSTANTS
# #PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/additionalData/' # change this to your path!
# PORT_NAME = "/dev/tty.usbserial-110" # change this to Arduino/teeny's port
# BAUD_RATE = 115200
# #RUNTIME_LENGTH = 120#570 # seconds

# bluesmirf = serial.Serial(port=PORT_NAME, baudrate=BAUD_RATE, rtscts=True)
# time.sleep(0.5) 
# msg = "$$$"
# print("sent: " + msg)
# bluesmirf.write(msg.encode(encoding="ascii"))
# time.sleep(0.1)
# while(1):
# 	#print(bluesmirf.in_waiting)
# 	nBytes = bluesmirf.in_waiting
# 	if (nBytes):
# 		received = bluesmirf.read(nBytes);
# 		print(received)

	# msg = input()