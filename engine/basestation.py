from . import Device

class BaseStation(Device):
    def __init__(self, id, env):
        self.env = env

        self.PRECISION = 0.001
        self._busy_time = self.env.now
        self.__current_packet = None
        super().__init__(id)
         

    def on_receive(self, packet):
        # this needs to resolve several problem
        # 1. collision among packets
        # 2. scheduling to send packet at timestamp + duration + fixed time
        # 3. message processing should be handled inside simpy loop

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
            self.process(packet)


    def process(self, packet):
        # this will be called only after the packet is successfuly received
        pass


    def run(self):
        while True:
            # base station is running at 0.001 precision
            yield self.env.timeout(self.PRECISION)
