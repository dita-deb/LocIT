from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json
import board
import busio
import adafruit_gps

# AWS IoT Core settings
host = "a25srdspphdz2u-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/raspberrypi/certs/"
clientId = "LocIT_RaspberryPi_Zero2W"
topic = "sensor"  # Topic to publish GPS data

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
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

# GPS Setup using I2C
i2c = busio.I2C(board.SCL, board.SDA)
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")  # Basic GGA and RMC info
gps.send_command(b"PMTK220,1000")  # 1 Hz update rate

# Conversion factors
METERS_TO_FEET = 3.28084
KNOTS_TO_MPH = 1.15078

# Main loop to send GPS data to AWS IoT
last_print = time.monotonic()

while True:
    gps.update()  # Make sure to call gps.update() each iteration
    current = time.monotonic()

if current - last_print >= 1.0:  # Print and send data every second
        last_print = current
        if not gps.has_fix:
            print("Waiting for fix...")
            continue  # Skip loop if no fix

        # Collect GPS data
        gps_data = {
            "timestamp": "{}/{}/{} {:02}:{:02}:{:02}".format(
                gps.timestamp_utc.tm_mon, gps.timestamp_utc.tm_mday, gps.timestamp_utc.tm_year,
                gps.timestamp_utc.tm_hour, gps.timestamp_utc.tm_min, gps.timestamp_utc.tm_sec
            ),
            "latitude": gps.latitude,
            "longitude": gps.longitude,
            "altitude_ft": gps.altitude_m * METERS_TO_FEET if gps.altitude_m is not None else None,
            "speed_mph": gps.speed_knots * KNOTS_TO_MPH if gps.speed_knots is not None else None
        }

        # Convert to JSON and publish to AWS IoT
        messageJson = json.dumps(gps_data)
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        print(f"Published topic {topic}: {messageJson}")

    time.sleep(1)
