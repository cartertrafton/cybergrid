#Test script for incrementing phase angle value, not used in main execution
import time

baseAngle = 0
lowerB = -180
upperB = 180
lts = time.time()
while True:
    ts = time.time()
    tsd = ts - lts
    print(baseAngle, "degrees %.20f\n" % tsd)
    if baseAngle == upperB:
        baseAngle = lowerB
    elif baseAngle >= lowerB:
        baseAngle = baseAngle + 1
    time.sleep(1/60)
    lts = time.time()