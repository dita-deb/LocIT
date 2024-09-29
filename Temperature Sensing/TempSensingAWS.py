from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import board
import busio
import adafruit_mcp9808

# AWS IoT Core settings
host = "a25srdspphdz2u-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/raspberrypi/certs/"
clientId = "TempMonitor_RaspberryPi_Zero2W"
topic = "sensor"

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(f"{certPath}RootCA1.pem", f"{certPath}TempMonitor_RaspberryPi_Zero2W.private.pem.key", f"{certPath}TempMonitor_RaspberryPi_Zero2W.cert.pem")

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)
myAWSIoTMQTTClient.connect()

# Initialize I2C and MCP9808 temperature sensor
i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c)

# Variable to track overheat mode status
overheat_mode = False

# Function to send temperature data to AWS IoT
def send_temperature_data(temp_fahrenheit, overheat_status):
    data = {
        "temperature_fahrenheit": temp_fahrenheit,
        "overheat_mode": overheat_status
    }
    message_json = json.dumps(data)
    myAWSIoTMQTTClient.publish(topic, message_json, 1)
    print(f"Published topic {topic}: {message_json}")

# Main loop to check temperature every 2 seconds and send to AWS IoT
while True:
    # Get the temperature in Celsius and convert to Fahrenheit
    temp_celsius = mcp.temperature
    temp_fahrenheit = (temp_celsius * 9 / 5) + 32
    print(f'Temperature: {temp_fahrenheit:.2f} degrees F')

    # Check for overheat condition
    if temp_fahrenheit > 85:
        overheat_mode = True
    elif temp_fahrenheit < 77:
        overheat_mode = False

    # If overheat mode is activated, print the message
    if overheat_mode:
        print("Overheat Mode: Activated")

    # Send temperature data and overheat status to AWS IoT
    send_temperature_data(temp_fahrenheit, overheat_mode)

    # Wait for 2 seconds before checking again
    time.sleep(2)
