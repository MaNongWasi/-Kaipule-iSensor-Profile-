import struct

types = {'0x0': 'undefined device', '0x1': 'IR fence', '0x2': 'PIR detector','0x3': 'natural gas detector',
         '0x4': 'panic button','0x5': 'smoke detector', '0x6': 'door sensor', '0x7': 'glass break detector',
         '0x8': 'vibration sensor', '0x9': 'water level detector', '0xa': 'high temperature sensor',
         '0xb': 'CO alarm', '0x16': 'doorbell button', '0x19': 'remote key fob', '0x1c': 'wireless keypad',
         '0x1e': 'wireless siren', '0x1f': 'remote swith'}


normal_device = ['0x0', '0x1', '0x2','0x3','0x5', '0x6', '0x7', '0x8', '0x9', '0xa', '0xb']
other_device = {'0x4': 2, '0x19': 3, '0x1e': 4, '0x1f': 5, '0x6':6}
events = {'0x0': 'close siren/close LED', '0x1': 'short siren sound', '0x2': 'siren sounds & LED flashes, but will close together in limited time',
       	  '0x5': 'short siren sound', '0x6': 'LED indicator normally flashes', '0x7': 'short siren sound & LED indicator normally flashes',
       	  '0x8': 'short siren sound & LED indicator off', '0x9': 'siren off & LED indicator flash once',
       	  '0xa': 'siren off & LED indicator flashes twice', '0xb': 'siren maintenance command'}

class iSensor:
    def __init__(self, data):
	self.typeD = data[0]
	self.eventD = data[1]
	self.controlD = data[2]	
	self.dict = {}
        self.event = ['', '', '', '']
	self.getType()
	
    def getType(self):
	typeID = hex(struct.unpack("B",self.typeD)[0] & 62)
	if typeID in types:
            type = types[typeID]
    	else:
            type = 'unknown device'

	self.dict['type'] = type
	self.getEvent(typeID) 

    def getEvent(self, typeID):
	protocol = 0
    	description = [0,0,0,0]
    	length = len(self.eventD)
    	i = length - 1
    	while i > 1:
            description[length-i-1] = self.eventD[i]
            i = i - 1
    	#print '\tdescription ', description
    	#print '\ttypeE ', typeID

    	if type in normal_device:
	    protocol = 1
	elif type in other_device:
            protocol = other_device[type]

    	if protocol == 1:
            getNormalProtocol(description)
#    	elif protocol == 2:
#            getPanicButton(description)
#    	elif protocol == 3:
#             getRemoteKey(description)
#    	elif protocol == 4:
#             getWirelesssiren(description)
#    	elif protocol == 5:
#             getRemoteSwitch(description)
#    	elif protocol == 6:
#            getDoorbellButton(description)
        self.dict['event'] = self.event
	self.getData()

    def getData(self):
	self.dict['data'] = struct.unpack("B",self.controlD)[0]

    def getNormalProtocol(self, d):
        #print d
        if d[3] == 1: #status report
            #print 'heartbeat signal'
            self.event[3]  = 'heartbeat signal'

        if d[2] == 0: #low voltage report
            #print 'normal battery level'
            self.event[2] = 'normal battery level'
        else:
            #print 'low battery'
            self.event[2] = 'low battery'

        if d[1] == 1:  #alarm
            #print 'alarm'
            self.event[1] = 'alarm'

        if d[0] == 0:  #anti-tamper
            #print 'normal status'
            self.event[0] = 'normal status'
        else:
            #print 'tamper alarm'
            self.event[2] = 'tamper alarm'

    def getPanicButton(self, d):
    	if d[1] == 0:  #button pressed
            #print 'button not pressed'
            self.event[1] = 'button not pressed'
    	else:
            #print 'button pressed'
            self.event[1] = 'button pressed'
  
    def getRemoteKey(self, d):
        if d[3] == 1: #SOS
            #print 'SOS'
            self.event[3]  = 'SOS'

        if d[2] == 1: #home arm key
            #print 'home arm'
            self.event[2] = 'home arm'

        if d[1] == 1:  #away arm key
            #print 'away alarm'
            self.event[1] = 'away alarm'

        if d[0] == 1:  #disarm key
            #print 'disarm'
            self.event[0] = 'disarm'

    def getWirelesssiren(self, d):
        #print events[d]
        self.event = [event[d], '', '', '']

def getRemoteSwitch(self, d):
    if d[3] == 0: #Main Control sends control code
        #print 'from Main Control'
        self.event[3]  = 'from Main Control'
    else: #controlled device responses its status
        #print 'from controlled deivce'
	self.event[3] =  'from controlled deivce'

    if d[2] == 0: #1. Main Control sends operation command to turn off switch  2. controlled switch off report
        #print 'switch off'
        self.event[2] = 'switch off'
    else: #1. Main Control sends operation command to turn on switch  2. controlled switch on report
        #print 'switch on'
        self.event[2] = 'switch on'

    def getDoorbellButton(self, d):
        if d[2] == 0: #battery level report
            #print 'normal battery level'
            self.event[2] = 'normal battery level'
	else:
            #print 'low battery level'
            self.event[2] = 'low battery level'

        if d[1] == 1:  #doorbell sounds
            #print 'press the button'
            self.event[1] = 'press the button'
        else:
            #print 'no press'
            self.event[1] = 'no press'

        if d[0] == 0:  #anti-tamper
            #print 'normal status'
            self.event[0] = 'normal status'
        else:
            #print 'tamper alarm'
            self.event[0] = 'tamper alarm'
