import time
import json
import board
import busio
import adafruit_mcp9808
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Core settings
host = "a25srdspphdz2u-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/raspberrypi/certs/"
clientId = "LocIT_RaspberryPi_Zero2W"
topic = "sensor"  # Topic to publish temperature data

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(
    "{}RootCA1.pem".format(certPath),
    "{}LocIT_RaspberryPi_Zero2W.private.pem.key".format(certPath),
    "{}LocIT_RaspberryPi_Zero2W-cert.pem.crt".format(certPath)
)


# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline publishing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

# Initialize I2C and sensor
i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c)
# Variable to track overheat mode status
overheat_mode = False

# Main loop to check temperature and send data to AWS IoT
while True:
    # Get the temperature in Celsius
    tempCelsius = mcp.temperature
    
    # Convert to Fahrenheit
    tempFahrenheit = (tempCelsius * 9 / 5) + 32
    
    # Check for overheat condition
    if tempFahrenheit > 77:
        overheat_mode = True
    elif tempFahrenheit < 74:
        overheat_mode = False
    
    # Print temperature and overheat status
    print(f'Temperature: {tempFahrenheit:.2f} degrees F')
    print(f'Overheat Mode: {"Active" if overheat_mode else "Inactive"}')
    
    # Prepare payload for AWS IoT
    payload = {
        'temperature_F': tempFahrenheit,
        'overheat_mode': overheat_mode
    }
    
    # Publish the payload to AWS IoT
    myAWSIoTMQTTClient.publish(topic, json.dumps(payload), 1)
    
    # Wait for 2 seconds before checking again
    time.sleep(2)
