from bootstrap import *

from protocols import TDMANode, TDMABaseStation

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
    parser = SimArg(description='TDMA protocol simulator')
    parser.add_argument("-tt", "-transmission", action="store", dest="transmission_time", default="0.99", type=float, help="set the transmission time per unit time")
    args = parser.parse_args()

    main(args.num_nodes, args.use_seed, args.sim_time, args.jitter_range, args.transmission_time)
