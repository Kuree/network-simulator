import simpy
import blinker
import logging
from pyns.engine.trace import TraceFormatter
import random

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
    def __init__(self, sender, timestamp, id, payload, duration, size, medium, frequency, ptx,
            valid = True, is_overhead = False, lat = 0, lng = 0):
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
        self.sender = sender
        self.timestamp = timestamp
        self.payload = payload
        self.id = id
        self.medium = medium
        self.duration = duration
        self.ptx = ptx
        self.is_overhead = is_overhead
        self.valid = valid
        self.size = size

        # this is needed for compute ber/path loss
        self.frequency = frequency

        self.coordinates = (lat, lng)


    def _get_delay(self, device):
        if self.medium.layer is None:
            return 0
        else:
            # transmitting at speed of light
            return self.medium.layer.get_distance(self.coordinates, device) / 299792458

    def _should_drop(self, device):
        if self.medium.layer is None or self.medium.layer.threshold is None:
            return False
        else:
            # compute the path loss
            layer = self.medium.layer
            loss = layer.get_path_loss(self.coordinates, device, self.frequency)
            # TODO: switch to PRX once it's done
            return loss > layer.threshold

    def _check_valid(self, receiver):
        if self.medium.layer is None:
            return self.valid
        else:
            rate = self.size / self.duration * 8 # bits per second
            layer = self.medium.layer
            ebn0 = layer.get_ebn0(self.ptx, self.sender, receiver, rate,
                self.frequency, self.medium.noise_figure, self.sender.gain, receiver.gain)
            per = layer.compute_per(ebn0, self.size)
            valid = receiver.random.uniform(0, 1) < per
            return valid


class TransmissionMedium:
    """This is the main medium that nodes transmit to.

    TransmissionMedium is the "medium" in MAC. It is the channel that each nodes need to send
    packet to.

    Attributes
    ----------
    env: simpy.Environment
        simpy simulation environment
    """
    def __init__(self, env, medium_name = "signal", layer = None, noise_figure=6):
        """Initialize the class

        Parameters
        ----------
        env: simpy.Environment
            simpy simulation environment
        medium_name: string, optional
            a unique name assigned to the transmission
        layer: PHY layer, optional
            if set, it provides physical layer information for the simulation.
        """
        self.env = env
        self.layer = layer
        self.noise_figure = 6
        self.__signal = blinker.signal(medium_name)

        # is_busy is useful for CSMA based protocol
        self.__is_busy = False
        self.__free_time = env.now

        self.__signal.connect(self._listen_busy)

        # this is used to hold the current transmission
        self.__current_packet = None

        # setup logging
        self.__loggers = []

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
        def _transmit(payload, duration, size, is_overhead, frequency):
            self.__transmit(device, payload, duration, size, is_overhead, frequency)
        device._medium.append((self, _transmit))

    def __subscribe(self, callback):
        self.__signal.connect(callback)

    def __transmit(self, device, payload, duration, size, is_overhead, frequency):
        """ called when device wants to transmit data
        """
        jitter = device.jitter()
        timestamp = self.env.now + jitter
        if timestamp < 0:
            timestamp = abs(jitter)
        self.__signal.send(TransmissionPacket(device, timestamp, device.id, payload, duration,
            size, self, is_overhead=is_overhead, frequency=frequency, ptx=device.ptx))


    def is_busy(self, device):
        """call when you need to know if the transmission is busy

        Note
        ----
        This is used internally by the simulatior. Device class should use its class method
        instead
        """
        channel_busy = self.env.now < self.__free_time
        if channel_busy:
            return self.__current_packet._check_valid(device)
        else:
            return False

    def _listen_busy(self, packet):
        duration = packet.duration
        self.__free_time = self.env.now + duration
        self.__current_packet = packet
        self.env.process(self._received_log(packet))

    def _received_log(self, packet):
        yield self.env.timeout(packet.duration)
        for logger in self.__loggers:
            logger.info(packet)


