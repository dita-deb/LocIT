import board
import busio
import adafruit_mcp9808

# Initialize I2C and sensor
i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c)

# Get the temperature in Celsius
tempCelsius = mcp.temperature

# Convert to Fahrenheit
tempFahrenheit = (tempCelsius * 9 / 5) + 32

# Print the temperature in Fahrenheit
print('Temperature: {:.2f} degrees F'.format(tempFahrenheit))
