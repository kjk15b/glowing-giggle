# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Wiring Check, Pi Radio w/RFM69

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import the RFM69 radio module.
import adafruit_rfm69
from elasticsearch import Elasticsearch
import datetime
import random

def get_data():
    # TODO: finish me!
    return {
        'sensor_1' : 100,
        'sensor_2' : 100,
        'sensor_3' : 100,
        'sensor_4' : 100,
    }

def get_mock_data():
    data = {
        'sensor_1' : random.randrange(100, 200),
        'sensor_2' : random.randrange(100, 200),
        'sensor_3' : random.randrange(100, 200),
        'sensor_4' : random.randrange(100, 200),
    }
    return data

def post(es : Elasticsearch, display : adafruit_ssd1306.SSD1306_I2C, index='barbecue-smoker'):
    print("Starting post")
    #display.fill(0)
    #display.show()
    data = get_mock_data()
    c = None
    # yyyy-MM-dd'T'HH:mm:ss
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    data['@timestamp'] = date_time
    print(data)
    print(es.ping())
    if es.ping():
        #display.text("Ingesting at: ", 0, 0, 1)
        #display.text(''.format(es.__str__()), display.width-85, display.height-7, 1)
        #display.show()
        c = es.index(index=index, body=data)
    else:
        #display.text("Failure to connect: ", 0, 0, 1)
        #display.text(''.format(es.__str__()), display.width-85, display.height-7, 1)
        #display.show()
        c = None
    return c


def setup_board():
    # Button A
    btnA = DigitalInOut(board.D5)
    btnA.direction = Direction.INPUT
    btnA.pull = Pull.UP
    # Button B
    btnB = DigitalInOut(board.D6)
    btnB.direction = Direction.INPUT
    btnB.pull = Pull.UP
    # Button C
    btnC = DigitalInOut(board.D12)
    btnC.direction = Direction.INPUT
    btnC.pull = Pull.UP
    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)
    # 128x32 OLED Display
    reset_pin = DigitalInOut(board.D4)
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
    # Clear the display.
    display.fill(0)
    display.show()
    width = display.width
    height = display.height
    # RFM69 Configuration
    CS = DigitalInOut(board.CE1)
    RESET = DigitalInOut(board.D25)
    #spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    try:
        #rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
        display.text('RFM69: Detected', 0, 0, 1)
        time.sleep(3)
        return None, display
    except RuntimeError as error:
        # Thrown on version mismatch
        display.text('RFM69: ERROR', 0, 0, 1)
        print('RFM69 Error: ', error)
        return None, display


def setup_elastic(index='barbecue-smoker', host='http://elasticsearch.attlocal.net:9200', auth=('elastic', 'kiesling')):
    es = Elasticsearch(hosts=host, http_auth=auth)
    print(es.__str__())
    if es.ping():
        #es.create(index=index, ignore=400)
        print("Success!")
    return es


if __name__ == '__main__':
    print("Starting Service!")
    #rfm69, display = setup_board()
    es = setup_elastic()
    print("Setup Complete!")
    while True:
        post(es, display=None)
        time.sleep(3)
    