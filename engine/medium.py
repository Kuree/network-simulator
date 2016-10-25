import simpy
import blinker
from .trace import TraceFormatter
import logging
import sys


class TransmissionPacket:
    def __init__(self, timestamp, id, payload, duration, rate = 1, valid = True, is_overhead = False):
        #self.env = env
        self.timestamp = timestamp
        self.payload = payload
        self.id = id
        self.duration = duration
        self.valid = True
        self.is_overhead = is_overhead

        self.size = duration * rate

class TransmissionMedium:
    PACKET_END = 0.001
    
    def __init__(self, env, medium_name = "signal"):
        self.env = env
        self.__signal = blinker.signal(medium_name)

        # is_busy is useful for CSMA based protocol
        self.__is_busy = False
        self.__free_time = env.now

        self.__signal.connect(self._listen_busy)

        # this is used to hold the current transmission
        self.__current_packet = None


        # setup logging
        self.logger = logging.getLogger(medium_name)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(TraceFormatter(env))
        self.logger.addHandler(ch)

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
        return self.env.now <= self.__free_time - TransmissionMedium.PACKET_END

    def _listen_busy(self, packet):
        duration = packet.duration
        if self.__free_time - TransmissionMedium.PACKET_END > self.env.now:
            self.__current_packet.valid = False
            packet.valid = False
            self.logger.debug(self.__current_packet)
        self.__free_time = self.env.now + duration
        self.__current_packet = packet
        self.logger.debug(packet)


