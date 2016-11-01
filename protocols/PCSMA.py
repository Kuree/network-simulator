from engine import Device, BaseStation

class CSMANode(Device):
    def __init__(self, id, env, p, seed, jitter_range, transmission_time):
        super().__init__(id, env, seed=seed, jitter_range=jitter_range)
        self.p = p
        self.transmission_time = transmission_time
        self.PRECISION = 0.05
        self.env.process(self.run()) 

    def run(self):
        yield self.env.timeout(self.random.random() * 10)
        dummy_payload = "CSMA"
        duration = self.transmission_time
        while True:
            prob = self.random.random() < self.p
            if not self.is_medium_busy() and prob:
                yield self.env.timeout(self.random.random() * self.PRECISION) # DELAY
                self.send(dummy_payload, duration = duration)
                yield self.env.timeout(duration)
            else:
                yield self.env.timeout(self.random.random() * self.PRECISION)


class CSMABaseStation(BaseStation):
    def __init__(self, id, env):
        super().__init__(id, env)

