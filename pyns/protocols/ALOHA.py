from pyns.engine import Device

class ALOHANode(Device):
    def __init__(self, id, env, rates,  seed, jitter_range, guard):
        MTU = rates[0] * (1 - guard * 2)
        super().__init__(id, env, rates, seed=seed, jitter_range=jitter_range, guard=guard, MTU = MTU)

    def _schedule_send(self, payload, duration, size, medium_index, is_overhead, antenna):
        with antenna.request() as req:
            yield req
            self._send(payload, duration, size, medium_index, is_overhead)
            self.should_send = False

        
class ALOHABaseStation(Device):
    def __init__(self, id, env, rates):
        super().__init__(id, env, rates)
        self.on_signal += Device._invalidate_packet_receive(self)
