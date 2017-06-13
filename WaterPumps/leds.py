# Author: Harold Clark
# Copyright Harold Clark 2017
#
try:
    import lib.uasyncio as asyncio
except ImportError:
    import uasyncio as asyncio
from utime import time
import machine
from WaterPumps.events import Event
from WaterPumps.monitors import monitor
class led(object):
    def __init__(self,ledPin=0, name='Not Defined'):
        """Init a single color led object"""
        self.powerPin = machine.Pin(ledPin, machine.Pin.OUT)
        self._name = name
        self.ledOnEvent = Event()
        self.ledOffEvent = Event()
        
    
    def name(self):
        return self._name
    
    async def monitorLED(self, debug=False):
        print('''%s - %s: monitorLED Started''' % (self.name(), time()))
        while True:
            if ledOnEvent.is_set():
                self.powerPin.value(True)
                ledOnEvent.clear()
            if ledOffEvent.is_set():
                self.powerPin.value(False)    
            await asyncio.sleep_ms(80)
    
    def registerOnEvent(self):
        return self.ledOnEvent
    
    def registerOffEvent(self):
        return self.ledOffEvent
    
class triLed(object):
    LED_BLUE = (True, False, True)
    LED_RED = (False, True, True)
    LED_GREEN = (True, True, False)
    LED_YELLOW = (False, True, False)
    LED_ORANGE = (False, False, True)
    LED_UNKNOWN = (True, False, False)
    LED_WHITE = (False, False, False)
    LED_OFF = (True, True, True)
    
    def __init__(self, redpin, bluepin, greenpin,name='Test', startColor=None):
        """Init a Tri color led object"""
        self.redPin = machine.Pin(redpin, machine.Pin.OUT)
        self.bluePin = machine.Pin(bluepin, machine.Pin.OUT)
        self.greenPin = machine.Pin(greenpin, machine.Pin.OUT)
        self.lastColor = None
        self.ledServerList  = []
        self._name = name
        self.flashEvent = Event()
        self.monitorObjects = []
        if startColor==None:
            self.setStartColor(self.LED_OFF)
        else:
            self.setStartColor(startColor)
        
    def name(self):
        return self._name
    
    def registerMonitorEvent(self, monitor):
        self.monitorObjects.append(monitor)
        return 1
    
    
    def setStartColor(self, color):
        R, B, G = color 
        self.redPin.value(R)
        self.bluePin.value(B)
        self.greenPin.value(G)    
    
    #maybe replaced need to look into hed 6/17/17    
    def registerLedClient(self, testTuple, index=0, debug=False):
        if len(testTuple)==4:
            self.ledServerList.insert(index, testTuple)
            if debug:
                print(len(self.ledServerList))
                print(self.ledServerList[-1])


    asyncio def monitorLED2(self, debug=False):
        print('''%s - %s: monitorLED Started''' % (self.name(), time()))
        mainLoop = asyncio.get_event_loop()
        mainLoop.create_task(self.setColor(self.LED_BLUE))
        while True:
            for c in self.monitorObjects:
                await asyncio.ms_sleep(50)
                if c.event.is_set():
                    self.launch(c)
                    c.event.clear()
            
            
    async def monitorLED(self, debug=False):
        """coroutine for monitor event to change the LED color"""        
        print('''%s - %s: monitorLED Started''' % (self.name(), time()))
        mainLoop = asyncio.get_event_loop()
        mainLoop.create_task(self.setColor(self.LED_BLUE))
        while True:            
            for pair, func, color, clear in self.ledServerList:
                v = True
                for event, test in pair:
                    v = event()==test and v
                    
                if v:
                    if debug:
                        print('''%s - %s: v is: %s, last color is: %s, current color is: %s''' % (self._name, time(), v, self.lastColor, color))
                    if self.lastColor!=color:
                        self.lastColor = color
                        mainLoop.create_task(func(color))
                        print('''%s - %s: added task to loop, color: %s''' % (self._name, time(), color))
                        if clear!=None:
                            clear.clear()
                        break
            await asyncio.sleep_ms(80)
            

    async def setColor(self, color):
        """set TriColor LED to pass color (RBG)"""
        R, B, G = color
        self.redPin.value(R)
        self.bluePin.value(B)
        self.greenPin.value(G)
        

    async def flash(self, color=None):
        import uasyncio as asyncio
        self.flashEvent.set()
        if color==None:
            color=self.LED_RED
        while self.flashEvent.is_set():
            self.setColor(color)
            await asyncio.sleep_ms(100)
            self.setColor(self.LED_OFF)
            await asyncio.sleep_ms(100)


    
    
