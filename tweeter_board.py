import requests
import serial

def main():

    arduino = serial.Serial("COM6") # COM Port may change

    while True:
        raw_msg = arduino.readline()
        msg_str = raw_msg.decode('ascii')
        msg = msg_str.rstrip()
        if msg == 'btn': # should match message from ARDUINO
            print("Button pressed")
            requests.get("http://justin.wattsworth.net/like.json?id=12")

main()