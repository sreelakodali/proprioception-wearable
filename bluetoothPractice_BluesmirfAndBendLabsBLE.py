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


# addrSMIRF_AC = "00:06:66:4E:48:AC"
# addrSMIRF_C0 = "00:06:66:4E:3E:C0"
#addrADSKit1 = "8FFC1F05-B314-208C-E078-BE9A13B256A6"

# BLEClientService        angms(0x1820);    // Angle Measurement Service
# BLEClientCharacteristic angmc(0x2a70);    // Angle Measurement Characteristic

async def main():
    # async def notification_handler(_, data):
    #     """Simple notification handler which prints the data received."""
    #     if (len(data) == 8):
    #         print("{}: {} {}".format(characteristic.description, data[0], data[4]))

    # def simple_callback(_, data):
    #     if(data.local_name == name):
    #         for s in data.service_uuids:
    #             if(int(s[0:8], 16) == BLEServiceAddr):
    #                 print("{}".format(data))
    #                 break


    # name = "Adafruit Bluefruit LE"
    # # BLEServiceAddr = 0x1820
    # # BLECharAddr = 0x2a70
    # device = await BleakScanner.find_device_by_name(name)
    # if device is None:
    #     print("could not find device with name {}".format(name))
    # else:
    #     print(device)

    #     async with BleakClient(device.address) as client:
    #         print("Connected! MTU size = {}".format(client.mtu_size))

            # set up calibration/configuration parameters, 1 axis, no stretching
            # ble_msg = 3;
            # angmc.write(&ble_msg, 1);

            # enable notification 

        #     for service in client.services:
        #         uuidService = int(service.uuid[0:8], 16)
        #         if(uuidService == BLEServiceAddr):
        #             print("Data Service {} found".format(hex(uuidService)))
        #             angms = service
        #             break

        #     for char in angms.characteristics:
        #         uuidChar = int(char.uuid[0:8], 16)
        #         if(uuidChar == BLECharAddr):
        #             print("Data Characteristic {} found".format(hex(uuidChar)))
        #             angmc = char
        #             break

        #     await client.start_notify(angmc, notification_handler)
        #     print("Notification started for characteristic")

        # scanner = BleakScanner(simple_callback)
        # while(1):
        #     async with scanner:
        #         await asyncio.sleep(1.0)
            # value = await client.read_gatt_char(angmc.uuid)
            # print("I/O Data Pre-Write Value: {0}".format(value))
            # await asyncio.sleep(0.5)
        # async with BleakScanner() as scanner:


  #   Bluefruit.Scanner.setRxCallback(scan_callback);
  # Bluefruit.Scanner.restartOnDisconnect(true);
  # Bluefruit.Scanner.setInterval(160, 80); // in unit of 0.625 ms
  # Bluefruit.Scanner.filterUuid(angms.uuid);
  # Bluefruit.Scanner.useActiveScan(false);
  # Bluefruit.Scanner.start(0);                   // 


            # for service in client.services:
            #     print("[Service] {}".format(str(service)))

            #     for char in service.characteristics:
            #         if "read" in char.properties:
            #             try:
            #                 value = await client.read_gatt_char(char.uuid)
            #                 extra = f", Value: {value}"
            #             except Exception as e:
            #                 extra = f", Error: {e}"
            #         else:
            #             extra = ""

            #         # if "write-without-response" in char.properties:
            #         #     extra += f", Max write w/o rsp size: {char.max_write_without_response_size}"

            #         print("  [Characteristic] {} ({}){}".format(char,",".join(char.properties),extra))

            #         # for descriptor in char.descriptors:
            #       
              #     try:
            #         #         value = await client.read_gatt_descriptor(descriptor.handle)
            #         #         print("    [Descriptor] {}, Value: {}".format(descriptor, value))
            #         #     except Exception as e:
            #         #         print("    [Descriptor] {}, Error: {}".format(descriptor, e))

        #     print("disconnecting...")

        # print("disconnected")
         # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#         print("Model Number: {0}".format("".join(map(chr, model_number))))

# asyncio.run(main(address))

    devices = await BleakScanner.discover()
    #print(len(devices))
    for d in devices:
        print(d.localName)

asyncio.run(main())

#8FFC1F05-B314-208C-E078-BE9A13B256A6: ads_eval_kit




# address = addrSMIRF_C0
# MODEL_NBR_UUID = "0x1101"

# async def main(address):
#     async with BleakClient(address) as client:
#         model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#         print("Model Number: {0}".format("".join(map(chr, model_number))))

# asyncio.run(main(address))



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