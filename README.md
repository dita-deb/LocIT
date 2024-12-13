# LocIT
Senior Design Project 2024  

## Overview  
LocIT, short for "Location Integrated Tracker," is a wearable safety device designed to enhance the security and monitoring of vulnerable individuals, such as children and elderly users. This project addresses real-world safety concerns with an innovative combination of hardware and software, offering real-time location tracking, facial recognition, geofencing, and more.

## Features  
- **GPS Location Tracking**: Accurate updates every 30 seconds with a 3-foot precision.
- **Temperature Monitoring**: Prevents device overheating by triggering shutdowns of non-essential components.
- **Vibrating Alerts**: Provides real-time notifications for geofence breaches or caregiver messages.
- **Gyroscope and Accelerometer**: Detects sudden movements or falls, notifying caregivers instantly.
- **Facial Recognition**: Identifies individuals near the wearer for added safety insights.
- **Geofencing**: Sends alerts when the user exits predefined safe zones.
- **Companion App**: Supports live tracking, notifications, and settings customization via FlutterFlow.

## Hardware System  
- **Sensors Subsystem**: Includes GPS, temperature, battery monitor, accelerometer, and gyroscope.
- **Actuators Subsystem**: Utilizes a vibration motor for silent notifications.
- **Communications Subsystem**: Transfers data securely via MQTT to AWS IoT Core and DynamoDB.
- **Power Subsystem**: Powered by a rechargeable LiPoly battery with over 24 hours of operation.
- **Central Processing Unit**: Raspberry Pi Zero 2 W for managing data, algorithms, and communication.

## Software System  
- Python-based main algorithm managing data collection, device state, and communication.
- AWS integration for real-time data storage and retrieval. [Backend-Webserver](https://02fydzyygd.execute-api.us-east-2.amazonaws.com/LocITDynamoDBDisplay)
- Companion app (FlutterFlow) for monitoring and control.

## Encasing Design  
- Constructed from PLA filament with 2 mm thickness for strength and durability.
- Compact dimensions: 2 inches wide, 4 inches long, and 2 inches deep.
- Three lid variations:
  - **No Slots Lid**: For fully enclosed design.
  - **4 Vents Lid**: Balanced ventilation and enclosure.
  - **9 Vents Lid**: Maximum cooling for high-temperature environments.

## Results  
- **High Accuracy**: GPS provides precise location tracking within a 3-foot radius.
- **Reliable Notifications**: Geofence breaches and fall detection alerts are delivered promptly.
- **Extended Usability**: Optimized power management ensures operation over a full day.

## Improvements and Optimizations  
Future enhancements include:
- Advanced facial recognition models for diverse conditions.
- Improved companion app usability with push notifications.
- Additional sensors for expanded functionality (e.g., heart rate monitoring).

## Getting Started  
Visit the [LocIT GitHub Repository](https://github.com/dita-deb/LocIT) for source code, hardware schematics, and additional documentation.

## License  
This project is licensed under a custom license. Redistribution, modification, or commercial use is restricted without explicit permission from the contributors. See the [LICENSE](LICENSE) file for more details.

## Contributors  
- **Anindita Deb** (dita-deb)  
- **Zachary Ponder** (ponder-zachary)  
- **Avery Porter** (Averyp119)
- **Damisi Kayode** (DamisiKayode0312)

## Acknowledgments  
Special thanks to Professor Jeffrey L. Yiin at Kennesaw State University for guidance and mentorship throughout the project.

---

*LocIT: Bringing peace of mind to caregivers while ensuring the safety of their loved ones.*
