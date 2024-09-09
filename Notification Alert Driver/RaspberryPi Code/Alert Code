import time
import board
import busio
import adafruit_drv2605
import serial

# Initialize I2C bus and DRV2605 module.
i2c = busio.I2C(board.SCL, board.SDA)
drv = adafruit_drv2605.DRV2605(i2c)

# Initialize serial communication
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1) #Pi Zero 2 W USB drive

effect_id = 1

while True:
    if ser.in_waiting > 0:
        # Read the serial input
        input_data = ser.readline().decode('utf-8').strip()
        
        if input_data == '1':
            print(f"Playing effect #{effect_id}")
            drv.sequence[0] = adafruit_drv2605.Effect(effect_id)  # Set the effect on slot 0.
            drv.play()  # Play the effect
            time.sleep(0.5)  # for 0.5 seconds
            drv.stop()  # Stop the effect
            
            # Increment effect ID and wrap back around to 1.
            effect_id += 1
            if effect_id > 123:
                effect_id = 1
