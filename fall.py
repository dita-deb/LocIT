import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
i2c = board.I2C() 
sensor = LSM6DSOX(i2c)
last_print = time.monotonic()
XMA,YMA,ZMA = 0, 0, 0
XMG,YMG,ZMG = 0, 0, 0
def fallcheck():
    global XMA, YMA, ZMA, XMG, last_print
    fall=False
    X1,Y1,Z1 = sensor.acceleration
    current = time.monotonic()
    XA,YA,ZA = sensor.gyro
    if XA>XMA:
	      XMA=XA
    if YA>YMA:
        YMA=YA
    if ZA>ZMA:
        ZMA=ZA
    if X1>XMG:
	      XMG=X1
    if ((XMA or YMA or ZMA) > 5) and ((XMG < -2.5) or (XMG > 2.5)):
	      fall=True
    if current - last_print >= 2.0:
        last_print = current
        XMA,YMA,ZMA = 0, 0, 0
        XMG=0
        print("test")
OH="off"
cnfg="locit/config.txt"
while True:
    try:
        with open(cnfg, 'r') as file:
            for line in file:
                if "Fall" in line:
                    OH=line.strip()           
                    OH=OH.replace('Fall ', '')
    except:
          None
    if OH=="On":
        fallcheck()
