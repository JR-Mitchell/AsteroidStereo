import serial
from time import sleep
path = "/dev/ttyACM0"
ser = serial.Serial(path, 9600, timeout=0.01, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()
ser.flushOutput()
sleep(4)
ser.write(bytes(b'..toggle..\n'))
