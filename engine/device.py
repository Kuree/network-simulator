import random
from collections import deque
import simpy
import math


class Device:
    PRECISION = 0.001
    ''' the base class for simulation node
    '''
    def __init__(self, id, env, rates, seed = 1, jitter_range = 0.01, guard = 0.01, MTU = 20):
        self.id = id
        self.env = env
        self.random = random.Random(seed)
        self._medium = []
        self.rates = rates
        self.__is_active = True
        self.jitter_range = jitter_range
        self._busy_time = self.env.now
        self.__current_packet = None
        self.guard = guard

        self.MTU = MTU

        self.__transmission_queue = deque([])

        self.antenna = simpy.Resource(env, capacity=1)

        self.env.process(self.__scheduler())

    def is_active(self):
        return self.__is_active

    def sleep(self):
        self.__is_active = False

    def wake_up(self):
        self.__is_active = True

    def _on_receive(self, packet):
        # this needs to resolve several problem
        # 1. collision among packets
        # 2. scheduling to send packet at timestamp + duration + fixed time
        # 3. message processing should be handled inside simpy loop
        if not self.__is_active:
            return
        timestamp = packet.timestamp
        duration = packet.duration
        if timestamp < self._busy_time:
            packet.valid = False
            if self.__current_packet is not None:
                self.__current_packet.valid = False

            # drop the packet. i.e. don't even bother to update the current packet
        else:
            self.__current_packet = packet
        
        self._busy_time = max(self._busy_time, timestamp + duration)

        # add to event queue
        self.env.process(self.wait_to_process(packet))
       
    def wait_to_process(self, packet):
        # pretending receiving the transmission
        time_to_sleep = packet.timestamp + packet.duration - self.env.now
        yield self.env.timeout(time_to_sleep)
        if packet.valid:
            self.on_receive(packet)

    def on_receive(self, packet):
        # this will be called only after the packet is successfuly received
        pass

    def jitter(self):
        ''' return the random jitter for the device
        '''
        jitter = (self.random.random() - 0.5) * self.jitter_range
        return jitter

    def _send(self, payload, duration, size, medium_index, is_overhead):
        if len(self._medium) == 0:
            raise Exception("Device has no medium attached")
        self._medium[medium_index][1](payload, duration, size, is_overhead)

    def send(self, payload, size, medium_index = 0):
        # TODO: fix rate
        # doing fragmentation here
        # NOTE: the actual payload won't be sliced into chunks
        #       this is for simulation only
        last_chunk = size % self.rates[0]
        chunks = [self.MTU for i in range(int(size // self.rates[0]))]
        if last_chunk != 0:
            chunks.append(last_chunk)
        for chunk in chunks:
            self.__transmission_queue.append((payload, chunk / self.rates[0], chunk, medium_index, False, self.antenna))

    def _get_queue_len(self):
        return len(self.__transmission_queue)

    def _compute_mtu(self, time, rate):
        return int(math.floor(rate * time))

    def _schedule_send(self, payload, duration, size, medium_index, is_overhead):
        # need to override this method for every protocol
        yield self.env.timeout(0)


    def __scheduler(self):
        while True:
            if len(self.__transmission_queue) == 0:
                yield self.env.timeout(Device.PRECISION)
            else:
                args = self.__transmission_queue.popleft()
                self.env.process(self._schedule_send(*args))

    def delay(self):
        # TODO: set the delay parameter
        delay_time = self.random.random() * 0.1
        yield self.env.timeout(delay_time)

    def is_medium_busy(self, medium_index = 0):
        self.env.process(self.delay())
        if len(self._medium) == 0:
            return False # if there is no medium attach to the device
        return self._medium[medium_index][0].is_busy()
