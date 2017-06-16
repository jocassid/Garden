#!/usr/bin/env python3

from time import sleep

from pyfirmata import Arduino
from pyfirmata.util import Iterator

# Temp Sensor
#--------------
# VCC   5V
# GND   Ground
# OUT   A0

# Water Sensor
#---------------
# +     3.3V
# -     Ground
# S     A1


TEMPERATURE_PIN = 0
WATER_PIN = 1

def readTemperature(board, pin):
    """Read temperature from an LM35 sensor with it's Vout pin attached to
    the specified analog pin.  Return result in degrees centigrade.
    
    Sensor outputs 10 mv per degree C
    
    Datasheet located at http://www.ti.com/lit/ds/symlink/lm35.pdf"""
    
    millivolts = board.analog[pin].read()
    if millivolts is None:
        print('Unable to read pin %d' % pin)
        return 0
    millivolts *= 5000
    return millivolts / 10.0
    
def readTempAndHumidity():
    """That sensor is probably one of these https://www.adafruit.com/product/386"""
    pass    
    
    

def main():
    board = Arduino('/dev/ttyACM0')
    iterator = Iterator(board)
    iterator.start()
    
    board.analog[TEMPERATURE_PIN].enable_reporting()
    board.analog[WATER_PIN].enable_reporting()
    sleep(1)
    
    value = board.analog[WATER_PIN].read()
    print('pin value is', value)
    
    #degreesC = readTemperature(board, TEMPERATURE_PIN)
    #print('The temperature is %.2F degrees C' % degreesC)
    
    
    
    # Setting iterator.board to None causes the iterator thread to exit
    iterator.board = None

if __name__ == '__main__':
    main()







