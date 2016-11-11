import simpy
from . import TransmissionMedium

class Simulator:
    # this class defines the common method for a standard simulator
    def __init__(self, name, total_time):
        self.env = simpy.Environment()
        self.total_time = total_time
        self.nodes = []    
        self.t = TransmissionMedium(self.env, name)
        
    def run(self):
        self.env.process(self._run())

        self.env.run(until=self.total_time)

    def _run(self):
        pass

    def add_logger(self, logger):
        self.t.add_logger(logger)
