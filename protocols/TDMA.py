from engine import Device 

class TDMANode(Device):
    def __init__(self, id, scheduled_time, total, env, rates, guard, seed, jitter_range):
        ''' schedule time is when the node should transmit
            it is computed by now % tatal == scheduled_time
        '''
        MTU = rates[0] * (1 - guard * 2)
        super().__init__(id, env, rates, seed=seed, jitter_range = jitter_range, guard = guard, MTU = MTU)
        self.scheduled_time = scheduled_time
        self.total = total

    def _schedule_send(self, payload, duration, size, medium_index, is_overhead, antenna):
        with antenna.request() as req:
            yield req
            if self.env.now % self.total < self.scheduled_time:
                next_basetime = self.env.now - self.env.now % self.total
            else:
                next_basetime = self.env.now - (self.env.now % self.total) + self.total 
            scheduled_time = next_basetime + self.scheduled_time + self.guard
            sleep_time = scheduled_time - self.env.now
            yield self.env.timeout(sleep_time)
            self._send(payload, duration, size, medium_index, is_overhead)
            yield self.env.timeout(duration)
            self.should_send = False

class TDMABaseStation(Device):
    def __init__(self, id, env, rates):
        super().__init__(id, env, rates)

        # nothing to be done here
