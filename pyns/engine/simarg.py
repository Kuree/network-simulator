import argparse

class SimArg(argparse.ArgumentParser):
    def __init__(self, description, remove_num=False):
        super().__init__(description)
        if not remove_num:
            self.add_argument("-n", "-num", action="store", type=int, default=100, dest="num_nodes", help="number of the nodes")
        self.add_argument("-s", "-seed", action="store_true", dest="use_seed", help="if present, force the simulation use pre-determined seed")
        self.add_argument("-t", "-time", action="store", dest="sim_time", default=10000, type=float, help="set the total simulation time")
        #self.add_argument("-j", "-jitter", action="store", dest="jitter_range", default="0.01", type=float, help="set the jitter range in unit time")
        #self.add_argument("-pr", "-packet_rate", action="store", dest="packet_rate", default=0.05, type=float, help="how likely the node will send a packet while idle")

        # we can add different rate to the system
        self.add_argument("--r", "--rates", action="store", dest="rate", default=[30], nargs="+", type=float, help="provide a list of available transmission date rate e.g. 20 bytes/s")

        # TODO: use reflection to load all protocols
        self.add_argument("-type", action="store", dest="type", required=True, type=int, help=self.get_protocol_help())
        self.add_argument("-stdout", action="store_true", dest="stdout", default=False, help="if set, the logger will print the result to stdout")

        self.add_argument("-test", action="store_true", dest="test", default=False, help="if set, it will tell the simulator that it's a test case")


    def get_protocol_help(self):
        # try to load the protocol type here
        from pyns.protocols import ProtocolType
        result_str = []
        for protocol_type in ProtocolType:
            result_str.append("{0}: {1}".format(protocol_type.value, protocol_type.name))
        return "choose which protocol to use. {0}".format(", ".join(result_str))

