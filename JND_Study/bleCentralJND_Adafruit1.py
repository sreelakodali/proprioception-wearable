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
import socket
from itertools import count, takewhile
from typing import Iterator
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import skBLESupport_JND as skB



# CONSTANTS
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!

#DIRECTORY
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = PATH +fileName+'/'
if not (os.path.exists(p)):
    os.makedirs(p)
    print("New directory created: %s" % fileName)
f = open(p + 'raw_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
#writer = csv.writer(f)

addr_Adafruit2 = "380FFB6A-AB04-7634-8A6C-C8E255F7A26C"
UART_SERVICE_UUID_BLE2 = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID_BLE2 = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" # 2, RX write
UART_TX_CHAR_UUID_BLE2 = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" # 3, TX notify
# UART_RX_CHAR_UUID_BLE2 = "00002901-0000-1000-8000-00805f9b34fb" # 2, RX write
# UART_TX_CHAR_UUID_BLE2 = "00002901-0000-1000-8000-00805f9b34fb" # 3, TX notify

#adafruit1 D5D630F2D088CDAC
#adafruit2 0D2286A72F3B189B

addr_Adafruit1 = "026B8104-5A8F-E8AF-518E-B778DB1C9CE2"
UART_SERVICE_UUID_BLE1 = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID_BLE1 = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" # 2, RX write
UART_TX_CHAR_UUID_BLE1 = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" # 3, TX notify
name = "Adafruit Bluefruit LE"
databuf = ""

async def quickScan():
    devices = await BleakScanner.discover()
    #print(len(devices))
    for dev in devices:
        # if (dev.name == name):
        print(dev)

# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))

def sendMySetpoints():
    data = "x2\n"
    s = data.encode(encoding="ascii")
    
    w = 0
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
    while (datetime.datetime.now() < endTime):
        #await asyncio.sleep(0.01)
        w = w + 1
    return(s)
                   

async def main():
    
    device = await BleakScanner.find_device_by_address(addr_Adafruit1)
    #device = await BleakScanner.find_device_by_name(name)
    if device is None:
        print("could not find device with name {}".format(name))
    else:
        print(device)

        
        # printing the data received from BLE uart. for packets that
        # get separated, they're concatenated accordingly with newline
        # character as demarker of end of packet
        def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
            global databuf
            global f
            if (True):
                strData = data.decode("ascii")
                if (strData[-1] == "\n"):
                    print(databuf+strData[:-1])
                    f.write(databuf+strData)
                    #writer.writerow([databuf+strData[:-1]])
                    databuf = ""
                else:
                    databuf += strData


        async with BleakClient(device.address) as client:
            print("Connected! MTU size = {}".format(client.mtu_size))

            await client.start_notify(UART_TX_CHAR_UUID_BLE1, handle_rx)
            loop = asyncio.get_running_loop()
            nus = client.services.get_service(UART_SERVICE_UUID_BLE1)
            rx_char = nus.get_characteristic(UART_RX_CHAR_UUID_BLE1)         
            

            while True:
                await asyncio.sleep(0.01)

                # for i in data:
                #     s = str(i).encode(encoding="ascii")
                #     await asyncio.sleep(0.01)
                #     print("sent:", s)
                #     await client.write_gatt_char(rx_char, s)
                #     #print(type(s))
                #     await skB.waitSK(10)
                  #data = input()
                  #print("Sending: " + str(data))
                  #data = data.encode(encoding="ascii")
                  #await client.write_gatt_char(rx_char, data, response=False)
                # This waits until you type a line and press ENTER.
                # A real terminal program might put stdin in raw mode so that things
                # like CTRL+C get passed to the remote device.

                #data = await loop.run_in_executor(None, sys.stdin.buffer.readline)
                data = await loop.run_in_executor(None, sendMySetpoints)


            # data will be empty on EOF (e.g. CTRL+D on *nix)
                if not data:
                    break

            #     # Writing without response requires that the data can fit in a
            #     # single BLE packet. We can use the max_write_without_response_size
            #     # property to split the data into chunks that will fit.
            #     #data = data.rstrip()
                for s in sliced(data, rx_char.max_write_without_response_size):
                    #print(s)
                    await client.write_gatt_char(rx_char, s, response=False)

                if (data.isascii()):
                    strSentData = data.decode("ascii")
                    if "fin" in strSentData:
                        print("done")
                        f.close()
                        break
                    else:
                        print("sent:", data)
                        f.write(strSentData)
                        #writer.writerow(strSentData)

            # for char in nus.characteristics:
            #     print(char)

asyncio.run(main())


# explorer
# async with BleakClient(device) as client:

#             for service in client.services:
#                 print("[Service] %s", service)

#                 for char in service.characteristics:
#                     if "read" in char.properties:
#                         try:
#                             value = await client.read_gatt_char(char.uuid)
#                             extra = f", Value: {value}"
#                             print(extra)
#                         except Exception as e:
#                             extra = f", Error: {e}"
#                     else:
#                         extra = ""

#                     if "write-without-response" in char.properties:
#                         extra += f", Max write w/o rsp size: {char.max_write_without_response_size}"
#                         print(extra)

#                     for descriptor in char.descriptors:
#                         try:
#                             value = await client.read_gatt_descriptor(descriptor.handle)
#                             print("    [Descriptor] %s, Value: %r", descriptor, value)
#                         except Exception as e:
#                              a = 0 #("    [Descriptor] %s, Error: %s", descriptor, e)


