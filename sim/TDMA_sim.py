import bootstrap

import simpy
import logging
import random
import argparse
from protocols import TDMANode, TDMABaseStation
from engine import TransmissionMedium

def main(num_nodes, use_seed, sim_time, jitter_range, transmission_time):
    env = simpy.Environment()
    t = TransmissionMedium(env)

    logger = logging.getLogger("signal")
    logger.setLevel(logging.DEBUG)

    bs = TDMABaseStation(0, env)
    t.add_device(bs)

    # create 100 nodes
    TOTAL = num_nodes
    for i in range(1, TOTAL + 1):
        seed = i if use_seed else random.randint(0, num_nodes * 100)
        node = TDMANode(i, i-1, TOTAL, env, 
                seed = seed, jitter_range=jitter_range, transmission_time = transmission_time)
        t.add_device(node)

    env.run(until=sim_time)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TDMA protocol simulator')
    parser.add_argument("-n", "-num", action="store", type=int, default=100, dest="num_nodes", help="number of the nodes")
    parser.add_argument("-s", "-seed", action="store_true", dest="use_seed", help="if present, force the simulation use pre-determined seed")
    parser.add_argument("-t", "-time", action="store", dest="sim_time", default=10000, type=float, help="set the total simulation time")
    parser.add_argument("-j", "-jitter", action="store", dest="jitter_range", default="0.01", type=float, help="set the jitter range in unit time")
    parser.add_argument("-tt", "-transmission", action="store", dest="transmission_time", default="0.99", type=float, help="set the transmission time per unit time")
    args = parser.parse_args()

    main(args.num_nodes, args.use_seed, args.sim_time, args.jitter_range, args.transmission_time)
