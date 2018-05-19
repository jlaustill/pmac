from gpiozero import Button, PWMLED
from signal import pause
from w1thermsensor import W1ThermSensor
from time import sleep
import RPi.GPIO as GPIO
import I2C_LCD_driver
import json
import threading
import os
import sys

config_file = os.path.join(sys.path[0], './config.json')
outsideTemp = 0
insideTemp = 0
fan_on = False

with open(config_file) as cf:
    config = json.load(cf)

lcd = I2C_LCD_driver.lcd()
outsideSensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, config["outside_sensor_id"])
insideSensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, config["inside_sensor_id"])

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)

def save_config():
    with open(config_file, 'w') as cf:
        json.dump(config, cf)

def turn_fan_on():
    GPIO.output(17, GPIO.HIGH)
    
def turn_fan_off():
    GPIO.output(17, GPIO.LOW)

def update_outsideTemp():
    global outsideTemp
    outsideTemp = outsideSensor.get_temperature(W1ThermSensor.DEGREES_F)
    
def update_insideTemp():
    global insideTemp
    insideTemp = insideSensor.get_temperature(W1ThermSensor.DEGREES_F)

def update_lcd():
    global outsideTemp,insideTemp,config,fan_on
    while True:
        lcd.lcd_display_string("Outside Temp: %.1f  " % outsideTemp, 1)
        lcd.lcd_display_string("Inside Temp:  %.1f  " % insideTemp, 2)
        lcd.lcd_display_string("Desired Temp: %.1f  " % config["low_temp"], 3)
        lcd.lcd_display_string("Fan on: %s  " % fan_on, 4)
        sleep(2)
    
lcd_thread = threading.Thread(target=update_lcd, args=())
lcd_thread.daemon = True
lcd_thread.start()

def lower_temp():
    global config
    if config["low_temp"] > 32.1:
        config["low_temp"] -= 0.1
        save_config()

def raise_temp():
    global config
    if config["low_temp"] < 100.1:
        config["low_temp"] += 0.1
        save_config()
        
def update_fan():
    global outsideTemp, insideTemp, config, fan_on
    if insideTemp - outsideTemp > 1 and insideTemp > float(config["low_temp"]):
        fan_on = True
    else:
        fan_on = False

buttonDown = Button(4)
buttonUp = Button(14)

buttonDown.when_pressed = lower_temp
buttonUp.when_pressed = raise_temp

while True:
    update_insideTemp()
    update_outsideTemp()
    update_fan()
    if fan_on:
        turn_fan_on()
    else:
        turn_fan_off()
    sleep(1)