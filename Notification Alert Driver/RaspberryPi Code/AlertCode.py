import time
import board
import busio
import adafruit_drv2605

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the DRV2605 motor driver
drv = adafruit_drv2605.DRV2605(i2c)

# Function to activate vibration
def vibrate():
    for _ in range(3):
        drv.sequence[0] = adafruit_drv2605.Effect(1)  # We can change the vibration effect
        drv.play()  # Play the sequence
        time.sleep(1)  # Wait 1 second between vibrations
        drv.stop()  # Stop the motor

# Main program loop
while True:
    user_input = input("Enter '1' to trigger vibration or 'q' to quit: ")

    if user_input == '1':
        print("Triggering vibration...")
        vibrate()
    elif user_input.lower() == 'q':
        print("Exiting program.")
        break
    else:
        print("Invalid input, please enter '1' or 'q'.")
        
drv.stop()
