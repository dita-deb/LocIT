from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json
import board
import busio
import adafruit_drv2605

# AWS IoT Core settings
host = "a25srdspphdz2u-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/raspberrypi/certs/"
clientId = "LocIT_RaspberryPi_Zero2W"
topic = "sensor"

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
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)
myAWSIoTMQTTClient.connect()

# Initialize I2C bus and the DRV2605 motor driver
i2c = busio.I2C(board.SCL, board.SDA)
drv = adafruit_drv2605.DRV2605(i2c)

# Function to activate vibration three times
def vibrate():
    for _ in range(3):
        drv.sequence[0] = adafruit_drv2605.Effect(1)  # We can change this if needed
        drv.play()
        time.sleep(1)
        drv.stop()
        time.sleep(0.5)

# Callback function to handle incoming alerts
def alert_callback(client, userdata, message):
    print(f"Received message from topic {message.topic}: {message.payload}")
    
    # Decode the payload to string
    payload = message.payload.decode('utf-8')

    # Check if the payload equals "1"
    if payload == '1':  # This looks for the message being sent from AWS, we will need to mimic this on the flutter app
        print("Sending Alert...")
        vibrate()  # Activate vibration
        print("Wearer alerted successfully.")

# Subscribe to the "sensor" topic
myAWSIoTMQTTClient.subscribe(topic, 1, alert_callback)

# Initial waiting message
print("Waiting for alert...")

# Keep the program running to listen for alerts
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    drv.stop()
    myAWSIoTMQTTClient.disconnect()
