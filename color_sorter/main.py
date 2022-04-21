#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import Font
from  mindsensorsPYB import PPS58
from  mindsensorsPYB import EV3Matrix
from  mindsensorsPYB import DIST_ToF
from  mindsensorsPYB import EV3RFid
from  mindsensorsPYB import LINELEADER
from  mindsensorsPYB import TFTPACK
from  mindsensorsPYB import ABSIMU
from  mindsensorsPYB import IRThermometer
from  mindsensorsPYB import VOLT
from  mindsensorsPYB import PFMATE
from  mindsensorsPYB import SUMOEYES

import os
import sys
import time



def RfidTest() :
    # Create your objects here.
    ev3 = EV3Brick()
    rfid= EV3RFid(Port.S1,0x22)
    
    print(rfid.GetFirmwareVersion())
    print(rfid.GetDeviceId())
    print(rfid.readUID())
    '''
    rfid.WriteBlockString(0x04,"this is Ravi test")
    rfid.clearUID()
    print(rfid.ReadBlockArray(4))
    print(rfid.ReadBlockArray(4))
    while True :
        
        print(rfid.readUID())
        time.sleep(1)
    '''



RfidTest() 
