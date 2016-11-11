from bootstrap import *

from protocols import create_basestation, create_node, ProtocolType
import logging
import numpy
import sys
import random


class ConstantSimulator(Simulator):
    def __init__(self, total_time, use_seed, num_nodes, protocol_type, name, pr):
        super().__init__(name, total_time)
        if use_seed:
            seeds = [i for i in range(num_nodes + 1)]
            numpy.random.seed(0)
            random.seed(0)
        else:
            seeds = [random.randint(0, num_nodes * 1000) for i in range(num_nodes + 1)]
        special_args = {"seed": seeds[0]}
        
        bs = create_basestation(protocol_type, 0, self.env, "default.json", special_args)
        self.t.add_device(bs)

        self.pr = pr

        for i in range(num_nodes):
            special_arg = {"total": num_nodes, "scheduled_time": i, "seed": seeds[i]}
            n = create_node(protocol_type, i, self.env, "default.json", special_arg)
            self.nodes.append(n)
            self.t.add_device(n)


    def _run(self):
        rate = self.pr * len(self.nodes)
        dummy_payload = "Test"
        while True:
            num_of_trans = int(numpy.random.poisson(rate))
            nodes_to_trans = numpy.random.choice(self.nodes, num_of_trans)
            for n in nodes_to_trans:
                n.send(dummy_payload, n.MTU)
            yield self.env.timeout(1)

def main():
    parser = SimArg("Simulation with constant packet rate")
    args = parser.parse_args()

    medium_name = "const_rate"
    
    # setting up logger    
    total_time = args.sim_time
    use_seed = args.use_seed
    num_nodes = args.num_nodes
    pr = args.packet_rate
    protocol_type = args.type

    sim = ConstantSimulator(total_time, use_seed, num_nodes, protocol_type, medium_name, pr)
    
    logger = logging.getLogger(medium_name)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(TraceFormatter(sim.env))
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    
    sim.add_logger(medium_name)
    
    sim.run()
   



if __name__ == "__main__":
    main()
