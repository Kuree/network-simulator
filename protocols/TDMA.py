from engine import Device 

class TDMANode(Device):
    def __init__(self, id, scheduled_time, total, env, seed, jitter_range, transmission_time):
        ''' schedule time is when the node should transmit
            it is computed by now % tatal == scheduled_time
        '''
        super().__init__(id, env, seed=seed, jitter_range = jitter_range)
        self.scheduled_time = scheduled_time
        self.total = total
        self.transmission_time = transmission_time
        self.env.process(self.run())

    def send(self, payload, size, medium_index = 0):
        duration = self.transmission_time # to avoid jitter
        next_basetime = self.env.now - (self.env.now % self.total) + self.total
        scheduled_time = next_basetime + self.scheduled_time
        self._schedule_send(scheduled_time, payload, duration, size)

class TDMABaseStation(Device):
    def __init__(self, id, env):
        super().__init__(id, env)

        # nothing to be done here
