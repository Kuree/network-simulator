import simpy
import blinker
import logging
from pyns.engine.trace import TraceFormatter


class TransmissionPacket:
    """This is the class used to represent a packet sent to the medium
    
    Attributes
    ----------
    timestamp: float
        the simpy time when the packet is sent
    id: int
        packet id. used to trace and analyze traffic
    duration: float
        how long the packet takes to transmit
    is_overhead: bool
        if the packet is protocol overhead
    valid: bool
        if set to true, the packet will be marked as invalid
    size: int
        the size of packet in bytes
    """
    def __init__(self, timestamp, id, payload, duration, size, valid = True, is_overhead = False):
        """Initialize the TransmissionPacket class
        
        This should be used internally by the simulator. Other protocols are 
        suggested to read the attributes.

        Parameters
        ----------
        timestamp: float
            the simpy time when the packet is sent
        id: int
            packet id. used to trace and analyze traffic
        duration: float
            how long the packet takes to transmit
        size: int
            the size of packet in bytes
        valid: bool, optional
            if set to true, the packet will be marked as invalid
        is_overhead: bool, optional
            if the packet is protocol overhead
        """
        
        self.timestamp = timestamp
        self.payload = payload
        self.id = id
        self.duration = duration
        self.is_overhead = is_overhead
        self.valid = valid
        self.size = size

class TransmissionMedium:
    """This is the main medium that nodes transmit to.
    
    TransmissionMedium is the "medium" in MAC. It is the channel that each nodes need to send
    packet to.

    Attributes
    ----------
    env: simpy.Environment
        simpy simulation environment
    """
    def __init__(self, env, medium_name = "signal"):
        """Initialize the class

        Parameters
        ----------
        env: simpy.Environment
            simpy simulation environment
        medium_name: string, optional
            a unique name assigned to the transmission
        """
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
        """Adda a logger to the medium

        Parameters
        ----------
        logger_name: string
            the name of the logger
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        self.__loggers.append(logger)

    def add_device(self, device):
        ''' Adds a device to the transmission medium

        Parameters
        ----------
        device: Device
            Any device instance
        '''
        self.__subscribe(device._on_receive)
        def _transmit(payload, duration, size, is_overhead):
            self.__transmit(device, payload, duration, size, is_overhead)
        device._medium.append((self, _transmit))

    def __subscribe(self, callback):
        self.__signal.connect(callback)

    def __transmit(self, device, payload, duration, size, is_overhead):
        """ called when device wants to transmit data
        """
        jitter = device.jitter()
        timestamp = self.env.now + jitter
        if timestamp < 0:
            timestamp = abs(jitter)
        self.__signal.send(TransmissionPacket(timestamp, device.id, payload, duration, size, is_overhead=is_overhead))
        
    
    def is_busy(self):
        """call when you need to know if the transmission is busy
        
        Note
        ----
        This is used internally by the simulatior. Device class should use its class method
        instead
        """
        return self.env.now <= self.__free_time

    def _listen_busy(self, packet):
        duration = packet.duration
        self.__free_time = self.env.now + duration
        self.__current_packet = packet
        for logger in self.__loggers:
            logger.info(packet)


