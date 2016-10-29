import bootstrap

import simpy
import logging
from protocols import TDMANode, TDMABaseStation
from engine import TransmissionMedium

def main():
    env = simpy.Environment()
    t = TransmissionMedium(env)

    logger = logging.getLogger("signal")
    logger.setLevel(logging.DEBUG)

    bs = TDMABaseStation(0, env)
    t.add_device(bs)

    # create 100 nodes
    TOTAL = 100
    for i in range(1, TOTAL + 1):
        node = TDMANode(i, i-1, TOTAL, env, seed = i)
        t.add_device(node)


    env.run(until=10)

if __name__ == "__main__":
    main()
