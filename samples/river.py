from pyns.protocols import create_basestation, create_node, ProtocolType
from pyns.engine import Simulator, SimArg, TraceFormatter, TransmissionMedium
from pyns.phy import BPSK
import logging
import numpy
import sys
import random
import os
import json

class RiverSimulator(Simulator):
    def __init__(self, total_time, use_seed, protocol_type, log_prefix):
        super().__init__(total_time)
        self.use_seed = use_seed
        self.protocol_type = protocol_type
        self.log_prefix = log_prefix

        self.bs_name = log_prefix.split("-")[0]

    def _run(self, env, simulation_id):
        # load configure json
        with open("river/{0}.json".format(self.bs_name)) as f:
            configure = json.load(f)

        num_nodes = len(configure)

        if self.use_seed:
            seeds = [i for i in range(num_nodes)]
            numpy.random.seed(0)
            random.seed(0)
        else:
            seeds = [random.randint(0, num_nodes * 1000) for i in range(num_nodes + 1)]
        special_args = {"seed": seeds[0]}
        name = self.log_prefix + str(simulation_id)
        
        # add a PHY layer
        layer = BPSK(None) # no threshold so far

        t = TransmissionMedium(env, name, layer=layer)
        t.add_logger(name)
        
        bs = create_basestation(self.protocol_type, 0, env, configure[0], special_args)
        t.add_device(bs)
        
        nodes = []
        for i in range(1, len(configure)):
            config = configure[i]
            special_arg = {"total": len(configure) - 1, "scheduled_time": i, "seed": seeds[i]}
            n = create_node(self.protocol_type, i, env, config, special_arg)
            nodes.append(n)
            t.add_device(n)


        dummy_payload = "Test"
        while True:
            for n in nodes:
                size = random.randrange(24, 48)  # random payload size
                n.send(dummy_payload, size)
            sleep_time = 3 * 60 / 0.2 # each tick is 0.2 seconds # need to switch to Realistic Environment
            yield env.timeout(sleep_time)

def main():
    parser = SimArg("Simulation for the river sites")
    parser.add_argument("-num_run", dest="num_runs", default=1, help="number of runs")
    parser.add_argument("-station_name", dest="station_name", default="6530001", help="base station name")
    args = parser.parse_args()

    
    # setting up logger    
    total_time = args.sim_time
    use_seed = args.use_seed
    num_runs = args.num_runs
    bs_name = args.station_name
    #pr = args.packet_rate
    protocol_type = args.type

    log_prefix = bs_name + "-"
    if args.test:
        use_seed = True
        random.seed(0)
    else:
        rates = [0.1 / num_nodes * i for i in range(1, 21)]

    sim = RiverSimulator(total_time, use_seed, protocol_type, log_prefix)
        
    for run_id in range(num_runs):
        name = log_prefix + str(run_id)
        logger = logging.getLogger(name)
        if args.stdout or args.test:
            ch = logging.StreamHandler(sys.stdout)
        else:
            ch = logging.FileHandler(os.path.join("rate_log", str(protocol_type) + "-" + name))
        ch.setFormatter(TraceFormatter())
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)
        
 
    sim.start(range(num_runs))
   

if __name__ == "__main__":
    main()
