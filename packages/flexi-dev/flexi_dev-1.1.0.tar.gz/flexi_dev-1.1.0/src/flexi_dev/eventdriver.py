import logging
from struct import unpack
from .metadriver import MetaDriver

class EventDriver(MetaDriver):

    def __init__(self, device, methodprefix='e_', *args, **kwargs):
        super(EventDriver, self).__init__(device=device, methodprefix=methodprefix, *args, **kwargs)
        self.logger = logging.getLogger('flexi_dev.EventDriver')

    async def readFromDevice(self):
        etime = await self.f.read(16)
        etype = unpack('H', await self.f.read(2))[0]
        ecode = unpack('H', await self.f.read(2))[0]
        evalue = unpack('I', await self.f.read(4))[0]
        if etype not in [1,2,3]:
            return ('', {'etype':etype, 'ecode':ecode, 'evalue':evalue})

        mname = self.methodprefix + 'btn%d' % ecode
        return (mname, {'etype':etype, 'ecode':ecode, 'evalue':evalue})

