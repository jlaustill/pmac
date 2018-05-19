from gpiozero import Button, PWMLED
from signal import pause
import I2C_LCD_driver

lcd = I2C_LCD_driver.lcd()
led = PWMLED(17)

lowTemp = 35.0

def update_lcd():
    lcd.lcd_display_string("Outside Temp: %.1f" % 51.1000, 1)
    lcd.lcd_display_string("Inside Temp: %.1f" % 71.1000, 2)
    lcd.lcd_display_string("Desired Temp: %.1f" % lowTemp, 3)
    lcd.lcd_display_string("Hi Oliver :)", 4)

def lower_temp():
    global lowTemp
    if lowTemp > 32.1:
        lowTemp -= 0.1
    print(lowTemp)
    led.on()
    update_lcd()

def raise_temp():
    global lowTemp
    if lowTemp < 100.1:
        lowTemp += 0.1
    print(lowTemp)
    led.off()
    update_lcd()

buttonDown = Button(4)
buttonUp = Button(14)

buttonDown.when_pressed = lower_temp
buttonUp.when_pressed = raise_temp

pause()