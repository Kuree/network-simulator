import simpy
from . import TransmissionMedium
from multiprocessing import Process

class Simulator:
    # this class defines the common method for a standard simulator
    def __init__(self, total_time):
        self.total_time = total_time
       
    def start(self, args):
        process_list = []
        for arg in args:
            p = Process(target=self.run, args=(arg,))
            process_list.append(p)

        for p in process_list:
            p.start()
        for p in process_list:
            p.join()

    def run(self, *args):
        env = simpy.Environment()
        env.process(self._run(env, *args))
        env.run(until=self.total_time)

    def _run(self, env, *args):
        pass

    def setup_sim(self, name):
        env = simpy.Environment()
        t = TransmissionMedium(env, name)
        t.add_logger(name)
        return env, t

