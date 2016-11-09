import simpy
import blinker
import logging
from .trace import TraceFormatter


class TransmissionPacket:
    def __init__(self, timestamp, id, payload, duration, size = 1, valid = True, is_overhead = False):
        #self.env = env
        self.timestamp = timestamp
        self.payload = payload
        self.id = id
        self.duration = duration
        self.is_overhead = is_overhead
        self.valid = valid
        self.size = size

class TransmissionMedium:
    PRECISION = 0.001
    
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
        self.__loggers = [] 
        #= logging.getLogger(medium_name)
        #ch = logging.StreamHandler(sys.stdout)
        #ch.setLevel(logging.DEBUG)
        #ch.setFormatter(TraceFormatter(env))
        #self.logger.addHandler(ch)

    def add_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        self.__loggers.append(logger)

    def add_device(self, device):
        ''' this method adds a device to the transmission medium
        '''
        self.__subscribe(device._on_receive)
        def _transmit(payload, duration, size, is_overhead):
            self.__transmit(device, payload, duration, size, is_overhead)
        device._medium.append((self, _transmit))

    def __subscribe(self, callback):
        self.__signal.connect(callback)

    def __transmit(self, device, payload, duration, size, is_overhead):
        ''' called when device wants to transmit data
        '''
        jitter = device.jitter()
        timestamp = self.env.now + jitter
        if timestamp < 0:
            timestamp = abs(jitter)
        self.__signal.send(TransmissionPacket(timestamp, device.id, payload, duration, size, is_overhead=is_overhead))
        
    
    def is_busy(self):
        # TODO: fix the packet end
        return self.env.now <= self.__free_time - TransmissionMedium.PRECISION

    def _listen_busy(self, packet):
        duration = packet.duration
        self.__free_time = self.env.now + duration
        self.__current_packet = packet
        for logger in self.__loggers:
            logger.info(packet)


