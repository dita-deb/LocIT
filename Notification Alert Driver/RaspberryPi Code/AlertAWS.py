from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import board
import busio
import adafruit_drv2605

# AWS IoT Core settings
host = "a25srdspphdz2u-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/raspberrypi/certs/"
clientId = "Alert_RaspberryPi_Zero2W"
topic = "sensor"

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(f"{certPath}RootCA1.pem", f"{certPath}Alert_RaspberryPi_Zero2W.private.pem.key", f"{certPath}Alert_RaspberryPi_Zero2W.cert.pem")

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

# Function to activate vibration
def vibrate():
    for _ in range(3):
        drv.sequence[0] = adafruit_drv2605.Effect(1)  # Change effect as needed
        drv.play()
        time.sleep(1)
        drv.stop()

# Callback function to handle incoming alerts
def alert_callback(client, userdata, message):
    print(f"Received message from topic {message.topic}: {message.payload}")
    payload = json.loads(message.payload)
    
    if payload.get("alert") == "trigger_vibration":
        print("Triggering vibration alert...")
        vibrate()

# Subscribe to the "alert" topic
myAWSIoTMQTTClient.subscribe(topic, 1, alert_callback)

# Keep the program running to listen for alerts
print("Listening for alerts... Press Ctrl+C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    drv.stop()
    myAWSIoTMQTTClient.disconnect()
