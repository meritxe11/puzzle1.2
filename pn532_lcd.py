import RPi.GPIO as GPIO
from pn532 import *
import drivers
from time import sleep

display = drivers.Lcd()

if __name__ == '__main__':
    try:
        #pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        #pn532 = PN532_I2C(debug=False, reset=20, req=16)
        pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
        display.lcd_display_string("Found PN532",1)
        display.lcd_display_string("firmware version: {0}.{1}",2)
        sleep(1)

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
        #display.lcd_display_string("Waiting for",1)
        #display.lcd_display_string("RFID/NFC card...",2)
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            # Try again if no card is available.
            if uid is None:
                continue
            #uidstr = hex(i) for i in uid
            print('Found card with UID:', [hex(i) for i in uid])
            uidstr = ""
            for i in uid:
              print(hex(i))
              uidstr = uidstr + str(hex(i))
            print(uidstr)
            display.lcd_display_string("Found card, UID:", 1)
            display.lcd_display_string(uidstr, 2) 
            sleep(1)
    except KeyboardInterrupt:
    	# If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    	print("Cleaning up!")
    	display.lcd_clear()
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
