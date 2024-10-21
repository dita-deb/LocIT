import GPSIoT
import TemperatureAWS
# import notificationAWS
import time
import json
import threading

# def monitor_alerts():
    # Continuously check for alerts in a separate thread
   #  notificationAWS.myAWSIoTMQTTClient.subscribe(notificationAWS.topic, 1, notificationAWS.alert_callback)

def main():
    # Start a thread for alert monitoring
   #  alert_thread = threading.Thread(target=monitor_alerts)
   # alert_thread.daemon = True
   # alert_thread.start()

    # Connect to AWS IoT
    print("Connecting to AWS IoT...")
    GPSIoT.myAWSIoTMQTTClient.connect()
    print("AWS IoT Connected successfully!")

    while True:
        try:
            # Get the latest temperature and overheat mode
            temp_data = TemperatureAWS.get_temperature()  # Call the temperature function
                        
            # Get the latest GPS data
            gps_data = GPSIoT.get_gps_data()
          
            # Combine GPS and temperature data into one message
            if temp_data and gps_data:
                combined_data = {
                    "timestamp": gps_data["timestamp"],
                    "latitude": gps_data["latitude"],
                    "longitude": gps_data["longitude"],
                    "altitude_ft": gps_data["altitude_ft"],
                    "speed_mph": gps_data["speed_mph"],
                    "temperature_F": temp_data['temperature_F'],
                    "overheat_mode": temp_data['overheat_mode']
                }

                # Convert combined data to JSON and publish to AWS IoT
                messageJson = json.dumps(combined_data)
                print(f"Publishing to AWS IoT: {messageJson}")
                GPSIoT.myAWSIoTMQTTClient.publish(GPSIoT.topic, messageJson, 1)

            # Sleep for a while before the next loop iteration
            time.sleep(2)

        except Exception as e:
            print(f"Error occurred: {e}")
            break

if __name__ == "__main__":
    main()
    time.sleep(5)
