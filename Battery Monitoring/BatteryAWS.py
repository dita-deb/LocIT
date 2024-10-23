import time
import board
from adafruit_lc709203f import LC709203F
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

# Global variable for low battery mode
lowBatteryMode = False

class LC709203FSensor:
    def __init__(self, i2c, clientId, host, certPath, topic):
        self.sensor = LC709203F(i2c)
        
        # AWS IoT Core settings
        self.topic = topic

        # Init AWSIoTMQTTClient
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        self.myAWSIoTMQTTClient.configureEndpoint(host, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(
            "{}RootCA1.pem".format(certPath),
            "{}{}.private.pem.key".format(certPath, clientId),
            "{}{}-cert.pem.crt".format(certPath, clientId)
        )

        # Connect to AWS IoT
        self.myAWSIoTMQTTClient.connect()

    def get_battery_data(self):
        try:
            voltage = self.sensor.cell_voltage
            percent = self.sensor.cell_percent
            return voltage, percent
        except OSError:
            print("retry reads")
            return None, None

    def update_low_battery_mode(self, percent):
        global lowBatteryMode
        if percent is not None:
            if percent < 18.0:
                lowBatteryMode = True
            else:
                lowBatteryMode = False

    def send_to_aws(self, voltage, percent):
        if voltage is not None and percent is not None:
            payload = {
                "voltage": round(voltage, 3),
                "percent": round(percent, 1),
                "lowBatteryMode": lowBatteryMode
            }
            self.myAWSIoTMQTTClient.publish(self.topic, json.dumps(payload), 1)
            print("Data sent to AWS IoT: ", payload)

if __name__ == "__main__":
    i2c = board.I2C()  # uses board.SCL and board.SDA

    # Define AWS IoT configuration
    clientId = "LocIT_RaspberryPi_Zero2W"
    host = "a25srdspphdz2u-ats.iot.us-east-2.amazonaws.com"
    certPath = "/home/raspberrypi/certs/"
    topic = "battery"

    battery_sensor = LC709203FSensor(i2c, clientId, host, certPath, topic)

    # Get battery data, update mode, and send to AWS
    voltage, percent = battery_sensor.get_battery_data()
    battery_sensor.update_low_battery_mode(percent)
    battery_sensor.send_to_aws(voltage, percent)
