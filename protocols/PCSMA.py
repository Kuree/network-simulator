from engine import Device

class CSMANode(Device):
    def __init__(self, id, env, rates, p, seed, jitter_range, guard):
        MTU = rates[0] * (1 - guard * 2)
        super().__init__(id, env, rates, seed=seed, jitter_range=jitter_range, guard=guard, MTU = MTU)
        self.p = p
        self.DELAY = 0.05

    def _schedule_send(self, payload, duration, size, medium_index, is_overhead, antenna):
        with antenna.request() as req:
            yield req
            sent = False
            while not sent:
                prob = self.random.random() < self.p
                if not self.is_medium_busy() and prob:
                    yield self.env.timeout(self.random.random() * self.DELAY) # DELAY
                    self._send(payload, duration, size, medium_index, is_overhead)
                    sent = True
                else:
                    yield self.env.timeout(self.random.random() * self.PRECISION)

        
class CSMABaseStation(Device):
    def __init__(self, id, env, rates):
        super().__init__(id, env, rates)

