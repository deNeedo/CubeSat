import serial

port = "COM6"

s = serial.Serial(port)
while True:
    res = s.read()
    print(res)