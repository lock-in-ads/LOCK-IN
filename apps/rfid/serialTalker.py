import serial
import time


async def serial_port(mode: int):
    arduino = serial.Serial(port="COM4", baudrate=9600, timeout=3)
    time.sleep(3)

    if mode == 0:
        while True:
            if arduino.in_waiting > 0:

                line = arduino.readline().decode('utf-8').rstrip()

                if line.startswith("C"):
                    yield line
    elif mode == 1:
        while True:
            if arduino.in_waiting > 0:

                line = arduino.readline().decode('utf-8').rstrip()

                if line.startswith("C"):
                    return line
