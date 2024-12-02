	# Reading and Saving Serial Data from MCU via BLE
# Written by: Sreela Kodali (kodali@stanford.edu) 

import serial, datetime, csv, os, asyncio, time, sys
import numpy as np
#from scipy import signal 
from bleak import BleakScanner, BleakClient
from itertools import count, takewhile
from typing import Iterator
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


# CONSTANTS
PATH = '/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/' # change this to your path!

#DIRECTORY
fileName = str(datetime.datetime.now())[0:16] # default name is date and time
fileName = ((fileName.replace('/', '_')).replace(' ', '_')).replace(':','-')
p = PATH +fileName+'/'
if not (os.path.exists(p)):
    os.makedirs(p)
    print("New directory created: %s" % fileName)
f = open(p + 'raw_device1_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
g = open(p + 'raw_device2_' + fileName + '.csv', 'w+', encoding='UTF8', newline='')
#writer = csv.writer(f)

addr_Adafruit1 = "026B8104-5A8F-E8AF-518E-B778DB1C9CE2"
addr_Adafruit2 = "380FFB6A-AB04-7634-8A6C-C8E255F7A26C"
UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" # 2, RX write
UART_TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" # 3, TX notify
name = "Adafruit Bluefruit LE"
databuf = ""
databuf2 = ""
linebuf = ""

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

# printing the data received from BLE uart. for packets that
# get separated, they're concatenated accordingly with newline
# character as demarker of end of packet
def handle_rx1(_: BleakGATTCharacteristic, data: bytearray):
    global databuf
    global f
    global linebuf

    strData = data.decode("ascii")
    if (strData[-1] == "\n"):
        if (len(linebuf) != 0):
            print(linebuf)
            linebuf = ""
        linebuf += ("1,"+databuf+strData[:-2])

        #print("1,"+databuf+strData[:-2], end=",", flush=True)
        f.write(databuf+strData)
        #writer.writerow([databuf+strData[:-1]])
        databuf = ""
    else:
        databuf += strData

def handle_rx2(_: BleakGATTCharacteristic, data: bytearray):
    global databuf2
    global g
    global linebuf

    strData = data.decode("ascii")
    if (strData[-1] == "\n"):

        if (len(linebuf) != 0):
            linebuf = linebuf + ", "
        linebuf = linebuf + ("2,"+databuf2+strData[:-2])
        if (linebuf[0] == ","):
            linebuf = linebuf[2:]
        print(linebuf)
        linebuf = ""

        #print("2,"+databuf2+strData[:-2])
        g.write(databuf2+strData)
        #writer.writerow([databuf+strData[:-1]])
        databuf2 = ""
    else:
        databuf2 += strData


async def main():
    device1 = await BleakScanner.find_device_by_address(addr_Adafruit1)
    device2 = await BleakScanner.find_device_by_address(addr_Adafruit2)
    #device = await BleakScanner.find_device_by_name(name)


    if (device1 is None) or (device2 is None):
        print("could not find device with name {}".format(name))
    
    else:
        print(device1)
        print(device2)


        async with BleakClient(device1.address) as client1:
            async with BleakClient(device2.address) as client2:

                print("Connected Device 1! MTU size = {}".format(client1.mtu_size))
                print("Connected Device 2! MTU size = {}".format(client2.mtu_size))

                await client1.start_notify(UART_TX_CHAR_UUID, handle_rx1)
                await client2.start_notify(UART_TX_CHAR_UUID, handle_rx2)

                loop = asyncio.get_running_loop()

                nus1 = client1.services.get_service(UART_SERVICE_UUID)
                rx_char1 = nus1.get_characteristic(UART_RX_CHAR_UUID)

                nus2 = client2.services.get_service(UART_SERVICE_UUID)
                rx_char2 = nus2.get_characteristic(UART_RX_CHAR_UUID)

                while True:
                    await asyncio.sleep(0.01)

                    data = await loop.run_in_executor(None, sys.stdin.buffer.readline)

                # # data will be empty on EOF (e.g. CTRL+D on *nix)
                    if not data:
                        break

                #     # Writing without response requires that the data can fit in a
                #     # single BLE packet. We can use the max_write_without_response_size
                #     # property to split the data into chunks that will fit.
                #     #data = data.rstrip()
                    if (data.isascii()):

                        strSentData = data.decode("ascii")
                        if "fin" in strSentData:
                            print("done")
                            f.close()
                            g.close()
                            break

                        # device1 = X, device2 = Y
                        elif "x" in strSentData: # check if for device1 or device2
                            print("sent to device 1:", data)
                            f.write(strSentData)
                            await client1.write_gatt_char(rx_char1, data)

                            # for s in sliced(data, rx_char1.max_write_without_response_size):
                            #     #print(s)
                            #     await client1.write_gatt_char(rx_char1, s)


                        elif "y" in strSentData:
                            print("sent to device 2:", data)
                            g.write(strSentData)
                            await client2.write_gatt_char(rx_char2, data)
                            # for s in sliced(data, rx_char2.max_write_without_response_size):
                            #     #print(s)
                            #     await client2.write_gatt_char(rx_char2, s)
                            
                        else:
                            print(data)

                # for char in nus.characteristics:
                #     print(char)

asyncio.run(main())

