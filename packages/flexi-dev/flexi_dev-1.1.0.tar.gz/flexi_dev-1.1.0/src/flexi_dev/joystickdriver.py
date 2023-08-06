import logging
from struct import unpack
from .metadriver import MetaDriver

# possible types: taken from joystick.h
JS_EVENT_BUTTON = 0x01    # button pressed/released
JS_EVENT_AXIS = 0x02    # joystick moved
JS_EVENT_INIT = 0x80    # initial state of device

class JoystickDriver(MetaDriver):

    def __init__(self, device, methodprefix='js_', *args, **kwargs):
        super(JoystickDriver, self).__init__(device=device, methodprefix=methodprefix, *args, **kwargs)
        self.logger = logging.getLogger('flexi_dev.JoystickDriver')

    async def readFromDevice(self):
        etime = unpack('I', await self.f.read(4))[0]
        evalue = unpack('h', await self.f.read(2))[0]
        etype = unpack('B', await self.f.read(1))[0]
        enumber = unpack('B', await self.f.read(1))[0]

        mname = ''
        if etype & JS_EVENT_INIT:
            return ('', {'etype':etype, 'evalue':evalue, 'enumber':enumber})
        if etype & JS_EVENT_BUTTON:
            mname = 'btn%d' 
        if etype & JS_EVENT_AXIS:
            mname = 'axis%d'
        if not mname:
            return ('', {'etype':etype, 'evalue':evalue, 'enumber':enumber})
        mname = self.methodprefix + mname % enumber
        return (mname, {'etype':etype, 'evalue':evalue, 'enumber':enumber})
