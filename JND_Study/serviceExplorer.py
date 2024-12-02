
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


