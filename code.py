#!/usr/bin/env python3

"""Using TinyLoRa with a Si7021 Sensor.
"""
import time
import busio
import digitalio
import board
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
import requests
import codecs


# Create library object using our bus SPI port for radio
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    
# RFM9x Breakout Pinouts
cs = digitalio.DigitalInOut(board.D6)
irq = digitalio.DigitalInOut(board.D5)
rst = digitalio.DigitalInOut(board.D4)
    
# TTN Device Address, 4 Bytes, MSB
devaddr = bytearray([ 0x26, 0x01, 0x13, 0xC8 ])
    
# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray(
    [
    0x85, 0xA5, 0xC5, 0x1F, 0x8D, 0xA7, 0x2D, 0x41, 0x86, 0x71, 0x28, 0x5B, 0xCA, 0xFB, 0xC6, 0xF3
    ]
)
    
# TTN Application Key, 16 Bytess, MSB
app = bytearray(
    [
    0xAE, 0xE5, 0x75, 0xE8, 0x2B, 0x43, 0x04, 0xEA, 0x4F, 0x92, 0xFB, 0xF5, 0xA3, 0xE0, 0x5B, 0xE8
    ]
)
    
ttn_config = TTN(devaddr, nwkey, app, country="EU")
    
lora = TinyLoRa(spi, cs, irq, rst, ttn_config)
    
# Data Packet to send to TTN
data = bytearray(10)

while True:
    #sample data
    result = 5
    print(result)
    # Encode payload as bytes
    longitude = int(51.952610 * 1000000)
    latidue = int(7.62571 * 1000000)
    result_int = int(result)


    # print(int2bytes(longitude))
    data[3] = (longitude >> 24) & 0xFF
    data[2] = (longitude >> 16) & 0xFF
    data[1] = (longitude >> 8) & 0xFF
    data[0] = longitude & 0xFF

    data[7] = (latidue >> 24) & 0xFF
    data[6] = (latidue >> 16) & 0xFF
    data[5] = (latidue >> 8) & 0xFF
    data[4] = latidue & 0xFF

    data[9] = (result_int >> 8) & 0xFF
    data[8] = result_int & 0xFF

    print(data)

    # Send data packet
    print("Sending packet...")
    lora.send_data(data, len(data), lora.frame_counter)
    print("Packet Sent!")
    lora.frame_counter += 1
    time.sleep(20)

