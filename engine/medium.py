import simpy
import blinker
from device import Device

# this defines the transmission medium

class TransmissionPacket:
    def __init__(self, id, payload):
        self.env = env
        self.payload = payload
        self.id = id

class TransmissionMedium:
    def __init__(self, env, medium_name = "signal"):
        self.env = env
        self.__signal = blinker.signal(medium_name)

    def add_device(self, device):
        ''' this method adds a device to the transmission medium
        '''
        self.__subscribe(device.on_receive)
        def _transmit(payload):
            self.__transmit(device, payload)
        device.send = _transmit

    def __subscribe(self, callback):
        self.__signal.connect(callback)

    def __transmit(self, device, payload):
        ''' called when device wants to transmit data
        '''
        self.__signal.send(TransmissionPacket(device.id, payload))


if __name__ == "__main__":
    def r(obj):
        print(obj.id, obj.payload)

    env = simpy.Environment()
    t = TransmissionMedium(env)

    d = Device(1)
    d.on_receive = r
    t.add_device(d)
    d.send("yo")
