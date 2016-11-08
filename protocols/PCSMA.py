from engine import Device

class CSMANode(Device):
    def __init__(self, id, env, p, seed, jitter_range, transmission_time):
        super().__init__(id, env, seed=seed, jitter_range=jitter_range)
        self.p = p
        self.transmission_time = transmission_time
        self.PRECISION = 0.05
        self.env.process(self.run()) 

    def _schedule_send(self, payload, duration, size, medium_index, is_overhead):
        sent = False
        while not sent:
            prob = self.random.random() < self.p
            if not self.is_medium_busy() and prob:
                yield self.env.timeout(self.random.random() * self.PRECISION) # DELAY
                super()._schedule_send((self.env.now, payload, duration, size, medium_index, is_overhead))
                sent = True
            else:
                yield self.env.timeout(self.random.random() * self.PRECISION)

        
class CSMABaseStation(Device):
    def __init__(self, id, env):
        super().__init__(id, env)

