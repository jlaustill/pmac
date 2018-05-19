from gpiozero import Button, PWMLED
from signal import pause
from w1thermsensor import W1ThermSensor
from time import sleep
import I2C_LCD_driver

lcd = I2C_LCD_driver.lcd()
outsideSensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0317042d7bff")
insideSensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "0317207671ff")
led = PWMLED(17)

lowTemp = 35.0

def update_outsideTemp():
    global outsideTemp
    outsideTemp = outsideSensor.get_temperature(W1ThermSensor.DEGREES_F)
    
def update_insideTemp():
    global insideTemp
    insideTemp = insideSensor.get_temperature(W1ThermSensor.DEGREES_F)

def update_lcd():
    lcd.lcd_display_string("Outside Temp: %.1f" % outsideTemp, 1)
    lcd.lcd_display_string("Inside Temp: %.1f" % insideTemp, 2)
    lcd.lcd_display_string("Desired Temp: %.1f" % lowTemp, 3)
    lcd.lcd_display_string("Hi Oliver :)", 4)

def lower_temp():
    global lowTemp
    if lowTemp > 32.1:
        lowTemp -= 0.1
    print(lowTemp)
    led.on()

def raise_temp():
    global lowTemp
    if lowTemp < 100.1:
        lowTemp += 0.1
    print(lowTemp)
    led.off()

buttonDown = Button(4)
buttonUp = Button(14)

buttonDown.when_pressed = lower_temp
buttonUp.when_pressed = raise_temp

while True:
    update_insideTemp()
    update_outsideTemp()
    update_lcd()
    sleep(1)