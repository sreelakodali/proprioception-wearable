# ADAFRUIT Reading serial data from computer, parsing values, and then doing things

import usb_cdc

usb_cdc.enable(console=True, data=False)   # Enable just console for stdin and stdout

adafruit = usb_cdc.console

while True:
	s = supervisor.runtime.serial_bytes_available
	print(s)
	
	if (adafruit.in_waiting > 0):
		data = (adafruit.readline()).decode()
		if data.endswith("\r"): data = data[:-1]
		if data.endswith("\n"): data = data[:-1]

		print(data)
		data_list = data.split(" ")

		# do what you want with values

