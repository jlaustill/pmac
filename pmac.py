from gpiozero import Button, PWMLED
from signal import pause
from w1thermsensor import W1ThermSensor
from time import sleep
import RPi.GPIO as GPIO
import I2C_LCD_driver
import json
import threading

config_file = 'config.json'
outsideTemp = 0
insideTemp = 0

with open(config_file) as cf:
    config = json.load(cf)

lcd = I2C_LCD_driver.lcd()
outsideSensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, config["outside_sensor_id"])
insideSensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, config["inside_sensor_id"])

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)

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
    global outsideTemp,insideTemp,config
    while True:
        lcd.lcd_display_string("Outside Temp: %.1f" % outsideTemp, 1)
        lcd.lcd_display_string("Inside Temp: %.1f" % insideTemp, 2)
        lcd.lcd_display_string("Desired Temp: %.1f" % config["low_temp"], 3)
        lcd.lcd_display_string("Hi Oliver :)", 4)
        sleep(1)
    
lcd_thread = threading.Thread(target=update_lcd, args=())
lcd_thread.daemon = True
lcd_thread.start()

def lower_temp():
    global config
    if config["low_temp"] > 32.1:
        config["low_temp"] -= 0.1

def raise_temp():
    global config
    if config["low_temp"] < 100.1:
        config["low_temp"] += 0.1

buttonDown = Button(4)
buttonUp = Button(14)

buttonDown.when_pressed = lower_temp
buttonUp.when_pressed = raise_temp

while True:
    update_insideTemp()
    update_outsideTemp()
    if outsideTemp < insideTemp and insideTemp > float(config["low_temp"]):
        turn_fan_on()
    else:
        turn_fan_off()
    sleep(1)