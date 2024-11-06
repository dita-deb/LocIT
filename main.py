import GPSIoT
import TemperatureAWS
import BatteryAWS
import notificationAWS
import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
from datetime import datetime
from decimal import Decimal

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table_name = 'LocIT'
table = dynamodb.Table(table_name)

# Global variable for overheat mode
overheat_mode = False

def push_to_dynamodb(data):
    """Function to push combined data to DynamoDB."""
    try:
        # Convert all float values to Decimal
        data = {k: Decimal(str(v)) if isinstance(v, float) else v for k, v in data.items()}
        
        # Add the partition and sort keys
        data['sensorID'] = data.get('sensorID', 'combined_sensor')
        data['ts'] = int(time.time())  # Use the current epoch time as the sort key

        # Put item in DynamoDB
        table.put_item(Item=data)
        print("Successfully pushed data to DynamoDB:", data)
    except Exception as e:
        print(f"Error pushing data to DynamoDB: {e}")

def on_alert_message(client, userdata, message):
    """Callback for handling alert messages."""
    global overheat_mode
    payload = message.payload.decode('utf-8')
    
    if payload == '1':  # Trigger alert only if payload is "1"
        if not overheat_mode:
            print("Alert received. Activating alert callback...")
            notificationAWS.alert_callback(client, userdata, message)  # Trigger alert callback
        else:
            print("Tracker currently overheated. Unable to send alert.")

def main():
    # AWS IoT Core settings
    host = "a25srdspphdz2u-ats.iot.us-east-2.amazonaws.com"
    certPath = "/home/avery119/certs/"
    clientId = "LocIT_RaspberryPi_Zero2W"

    # Init AWSIoTMQTTClient
    client = AWSIoTMQTTClient(clientId)
    client.configureEndpoint(host, 8883)
    client.configureCredentials(
        "{}RootCA1.pem".format(certPath),
        "{}LocIT_RaspberryPi_Zero2W.private.pem.key".format(certPath),
        "{}LocIT_RaspberryPi_Zero2W-cert.pem.crt".format(certPath)
    )

    # AWSIoTMQTTClient connection configuration
    client.configureAutoReconnectBackoffTime(1, 32, 20)
    client.configureOfflinePublishQueueing(-1)  # Infinite offline publishing
    client.configureDrainingFrequency(2)  # Draining: 2 Hz
    client.configureConnectDisconnectTimeout(20)  # 20 sec
    client.configureMQTTOperationTimeout(20)  # 20 sec

    print("Connecting to AWS IoT...")
    client.connect()
    print("AWS IoT Connected successfully!")

    # Subscribe to the "alert" topic to handle alerts
    client.subscribe("alert", 1, on_alert_message)

    while True:
        try:
            # Get the latest temperature and overheat mode
            temp_data = TemperatureAWS.get_temperature(client)
            if temp_data:
                global overheat_mode
                overheat_mode = temp_data.get('overheat_mode', False)  # Update overheat_mode status
                print(f"Updated Overheat Mode: {'Active' if overheat_mode else 'Inactive'}")
            else:
                print("No temperature data received.")

            # Get the latest GPS data
            gps_data = GPSIoT.get_gps_data(client)
            if not gps_data:
                print("No GPS data received.")

            # Get the latest battery data
            battery_data = BatteryAWS.get_battery_power(client)
            if not battery_data:
                print("No battery data received.")

            # Combine GPS, temperature, and battery data into one message if all are available
            if temp_data and gps_data and battery_data:
                combined_data = {
                    "timestamp": gps_data["timestamp"],
                    "sensorID": "combined_sensor",
                    "latitude": gps_data["latitude"],
                    "longitude": gps_data["longitude"],
                    "altitude_ft": gps_data["altitude_ft"],
                    "speed_mph": gps_data["speed_mph"],
                    "temperature_F": temp_data['temperature_F'],
                    "overheat_mode": temp_data['overheat_mode'],
                    "battery_voltage": battery_data['battery_voltage'],
                    "battery_percent": battery_data['battery_percent'],
                    "low_battery_mode": battery_data['low_battery_mode']
                }

                # Convert combined data to JSON and publish to AWS IoT
                messageJson = json.dumps(combined_data)
                print(f"Publishing to AWS IoT: {messageJson}")
                client.publish("combined", messageJson, 1)

                # Push the same data to DynamoDB
                push_to_dynamodb(combined_data)

            # Sleep for a while before the next loop iteration
            time.sleep(20)

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            break

if __name__ == "__main__":
    main()
    time.sleep(5)
