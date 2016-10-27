from device import Device

class BaseStation(Device):
    def __init__(self, id, env):
        self.env = env
        super.__init__(id)


    def on_receive(self, packet):
        # this needs to resolve several problem
        # 1. collision among packets
        # 2. scheduling to send packet at timestamp + duration + fixed time
        pass
