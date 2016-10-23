import simpy
import blinker
from queue import Queue

# this defines the transmission medium

class TransmissionPacket:
    def __init__(self, timestamp, id, payload, duration):
        #self.env = env
        self.timestamp = timestamp
        self.payload = payload
        self.id = id
        self.duration = duration

class TransmissionMedium:
    def __init__(self, env, medium_name = "signal"):
        self.env = env
        self.__signal = blinker.signal(medium_name)

        # is_busy is useful for CSMA based protocol
        self.__is_busy = False
        self.__packet_queue = Queue()
        self.__free_time = env.now

        self.__signal.connect(self._listen_busy)

    def add_device(self, device):
        ''' this method adds a device to the transmission medium
        '''
        self.__subscribe(device._on_receive)
        def _transmit(payload, time):
            self.__transmit(device, payload, time)
        device._send = _transmit

        device._medium = self

    def __subscribe(self, callback):
        self.__signal.connect(callback)

    def __transmit(self, device, payload, time):
        ''' called when device wants to transmit data
        '''
        self.__signal.send(TransmissionPacket(self.env.now, device.id, payload, time))

    
    def is_busy(self):
        # TODO: fix the packet end
        PACKET_END = 0.001
        return self.env.now <= self.__free_time - PACKET_END

    def _listen_busy(self, packet):
        duration = packet.duration
        self.__free_time = self.env.now + duration


