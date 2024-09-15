import time
import board
import busio
import adafruit_gps

# For I2C, use the default pins for SCL and SDA on the Raspberry Pi.
i2c = busio.I2C(board.SCL, board.SDA)

# Create a GPS module instance using the I2C interface.
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

# Initialize the GPS module by changing what data it sends and at what rate.
# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# Set update rate to once a second (1hz).
gps.send_command(b"PMTK220,1000")

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()

# Conversion factors
METERS_TO_FEET = 3.28084
KNOTS_TO_MPH = 1.15078

while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            continue
        
        # We have a fix! Now print out the relevant information.
        print("=" * 40)  # Print a separator line.
        
        # Timestamp
        print(
            "Timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                gps.timestamp_utc.tm_mon,  
                gps.timestamp_utc.tm_mday,  
                gps.timestamp_utc.tm_year,  
                gps.timestamp_utc.tm_hour,  
                gps.timestamp_utc.tm_min,  
                gps.timestamp_utc.tm_sec,
            )
        )
        
        # Latitude and Longitude
        print("Latitude: {0:.6f} degrees".format(gps.latitude))
        print("Longitude: {0:.6f} degrees".format(gps.longitude))
        
        # Altitude (in feet)
        if gps.altitude_m is not None:
            altitude_ft = gps.altitude_m * METERS_TO_FEET
            print("Altitude: {:.2f} feet".format(altitude_ft))
        
        # Speed (in miles per hour)
        if gps.speed_knots is not None:
            speed_mph = gps.speed_knots * KNOTS_TO_MPH
            print("Speed: {:.2f} mph".format(speed_mph))
