import serial
import time

arduino = serial.Serial(port="COM4",baudrate=9600, timeout=3)

time.sleep(3)
contador = 0

while True:

    if arduino.in_waiting > 0:

        line = arduino.readline().decode('utf-8').rstrip()

        if line.startswith("C"):
            print(line)
