from engine import Device 

class TDMANode(Device):
    def __init__(self, id, scheduled_time, total, env, rates, seed, jitter_range, transmission_time):
        ''' schedule time is when the node should transmit
            it is computed by now % tatal == scheduled_time
        '''
        super().__init__(id, env, rates, seed=seed, jitter_range = jitter_range)
        self.scheduled_time = scheduled_time
        self.total = total
        self.transmission_time = transmission_time

    def _schedule_send(self, payload, duration, size, medium_index, is_overhead):
        duration = self.transmission_time # to avoid jitter
        next_basetime = self.env.now - (self.env.now % self.total) + self.total
        scheduled_time = next_basetime + self.scheduled_time
        sleep_time = scheduled_time - self.env.now
        yield self.env.timeout(sleep_time)
        self._send(payload, duration, size, medium_index, is_overhead)


class TDMABaseStation(Device):
    def __init__(self, id, env, rates):
        super().__init__(id, env, rates)

        # nothing to be done here
