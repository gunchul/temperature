#!/usr/bin/python
import sys
import time
from datetime import datetime
from sense_hat import SenseHat


def print_sens():
    now   = datetime.now()
    print "%s, %.2f, %.2f, %.2f" % ( now.strftime("%Y, %m, %d, %H, %M, %S")
                                   , sense.temperature
                                   , sense.humidity
                                   , sense.pressure )
    sys.stdout.flush()

sense = SenseHat()
run = 1
while (run!=0):
    print_sens()
    time.sleep(600)
