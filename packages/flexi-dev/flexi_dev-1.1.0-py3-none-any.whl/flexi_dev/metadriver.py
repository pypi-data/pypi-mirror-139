import trio
import logging

class MetaDriver():

    def __init__(self, device, methodprefix, *args, **kwargs):
        super(MetaDriver, self).__init__(*args, **kwargs)
        self.device = device
        self.methodprefix = methodprefix
        self.logger = logging.getLogger('flexi_dev.MetaDriver')
        self.stop = False

    async def defaultAction(self, **kwargs):
        s = " ".join([f"'{k}':'{v}'" for k, v in kwargs.items()])
        self.logger.debug(f'defaultAction: {s}')

    async def run(self):
        self.logger.info("Starting to listen to %s ..." % self.device)
        self.f = await trio.open_file(self.device, 'rb')
        while not self.stop:
            mname, kwargs = await self.readFromDevice()
            try:
                method = self.__getattribute__(mname)
            except AttributeError:
                await self.defaultAction(mname=mname, **kwargs)
                continue
            await method(**kwargs)
        await self.f.aclose()
        self.logger.info("Shutting down.")
