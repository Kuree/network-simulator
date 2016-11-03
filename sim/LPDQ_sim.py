from bootstrap import *

from protocols import LPDQNode, LPDQBaseStation

def main(args):
    num_nodes = args.num_nodes
    use_seed = args.use_seed
    env = simpy.Environment()
    t = TransmissionMedium(env)

    logger = logging.getLogger("signal")
    logger.setLevel(logging.DEBUG)

    bs_seed = 0 if use_seed else random.randint(0, num_nodes*1000)
    bs = LPDQBaseStation(0, env, bs_seed, args.m, args.rate, args.jitter_range,
            args.feedback_t, args.slot_t)
    t.add_device(bs)

    for i in range(1, num_nodes + 1):
        seed = i if use_seed else random.randint(0, num_nodes * 1000)
        node = LPDQNode(i, env, seed=seed, jitter_range=args.jitter_range, 
                rate = args.rate, m=args.m, packet_rate=args.packet_rate,
                slot_t = args.slot_t, feedback_t = args.feedback_t)
        t.add_device(node)
        


    env.run(until=args.sim_time)


if __name__ == "__main__":
    parser = SimArg(description="CSMA protocol simulator")
    parser.add_argument("-m", action="store", dest="m", default=3, type=int, help="number of mini-slots")
    parser.add_argument("-slot_t", action="store", dest="slot_t", default=0.1, type=float, help="duration of mini-stlos frame (total)")
    parser.add_argument("-feedback_t", action="store", dest="feedback_t", default=0.1, type=float, help="duration of feedback frame (total)")

    args = parser.parse_args()

    main(args)
 

