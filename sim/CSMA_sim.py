from bootstrap import * # need to replace this after using package

from protocols import CSMANode, CSMABaseStation

def main(num_nodes, use_seed, sim_time, jitter_range, transmission_time, p):
    env = simpy.Environment()
    t = TransmissionMedium(env)

    logger = logging.getLogger("signal")
    logger.setLevel(logging.DEBUG)

    bs = CSMABaseStation(0, env)
    t.add_device(bs)

    # create 100 nodes
    TOTAL = num_nodes
    for i in range(1, TOTAL + 1):
        seed = i if use_seed else random.randint(0, num_nodes * 1000)
        node = CSMANode(i, env, p,
                seed = seed, jitter_range=jitter_range, transmission_time = transmission_time)
        t.add_device(node)

    env.run(until=sim_time)



if __name__ == "__main__":
    parser = SimArg(description="CSMA protocol simulator")
    parser.add_argument("-tt", "-transmission", action="store", dest="transmission_time", default="0.99", type=float, help="set the transmission time")
    parser.add_argument("-p", action="store", dest="p", default=0.1, type=float, help="set the p-csma probabiilty")
    args = parser.parse_args()

    main(args.num_nodes, args.use_seed, args.sim_time, args.jitter_range, args.transmission_time, args.p)



