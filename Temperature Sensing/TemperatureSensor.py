import board
import busio
import adafruit_mcp9808
import time

# Initialize I2C and sensor
i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c)

# Variable to track overheat mode status
overheat_mode = False

# Loop to check temperature every 2 seconds
while True:
    # Get the temperature in Celsius
    tempCelsius = mcp.temperature
    
    # Convert to Fahrenheit
    tempFahrenheit = (tempCelsius * 9 / 5) + 32
    
# Print the temperature in Fahrenheit
    print('Temperature: {:.2f} degrees F'.format(tempFahrenheit))
    
    # Check for overheat condition
    if tempFahrenheit > 85:
        overheat_mode = True
    elif tempFahrenheit < 77:
        overheat_mode = False
    
    # If overheat mode is activated, print the message
    if overheat_mode:
        print("Overheat Mode: Activate")
    
    # Wait for 2 seconds before checking again
    time.sleep(2)

