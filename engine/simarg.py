import argparse

class SimArg(argparse.ArgumentParser):
    def __init__(self, description):
        super().__init__(description)
        self.add_argument("-n", "-num", action="store", type=int, default=100, dest="num_nodes", help="number of the nodes")
        self.add_argument("-s", "-seed", action="store_true", dest="use_seed", help="if present, force the simulation use pre-determined seed")
        self.add_argument("-t", "-time", action="store", dest="sim_time", default=10000, type=float, help="set the total simulation time")
        #self.add_argument("-j", "-jitter", action="store", dest="jitter_range", default="0.01", type=float, help="set the jitter range in unit time")
        self.add_argument("-pr", "-packet_rate", action="store", dest="packet_rate", default=0.05, type=float, help="how likely the node will send a packet while idle")

        # we can add different rate to the system
        #self.add_argument("--r", "--rate", action="store", dest="rate", default=[30], nargs="+", type=float, help="provide a list of available transmission date rate e.g. 20 bytes/s")

        self.add_argument("-type", action="store", dest="type", type=int, help="choose which protocol to use. 0: TDMA, 1: P-CSMA, 2: LPDQ")

