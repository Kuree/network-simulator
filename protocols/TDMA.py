#import bootstrap

from engine import Device, BaseStation, TransmissionMedium

class TDMANode(Device):
    def __init__(self, id, scheduled_time, total, env, seed = 1, jitter_range = 0.01):
        ''' schedule time is when the node should transmit
            it is computed by now % tatal == scheduled_time
        '''
        super().__init__(id, seed=seed, jitter_range = jitter_range)
        self.scheduled_time = scheduled_time
        self.total = total
        self.env = env

        self.env.process(self.run())


    def run(self):
        dummpy_payload = "1"
        duration = 0.99 # to avoid jitter
        while True:
            if self.env.now % self.total == self.scheduled_time:
                self.send(dummpy_payload, duration=duration)
            yield self.env.timeout(1)


class TDMABaseStation(BaseStation):
    def __init__(self, id, env):
        super().__init__(id, env)

        # nothing to be done here
