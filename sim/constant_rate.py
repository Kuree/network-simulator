from bootstrap import *

from protocols import create_basestation, create_node, ProtocolType
import logging
import numpy
import sys

def sending(nodes, pr, env):
    rate = pr * len(nodes)
    dummy_payload = "Test"
    while True:
        num_of_trans = int(numpy.random.poisson(rate))
        nodes_to_trans = numpy.random.choice(nodes, num_of_trans)
        for n in nodes_to_trans:
            n.send(dummy_payload, 20)
        yield env.timeout(1)

def main():
    parser = SimArg("Simulation with constant packet rate")
    args = parser.parse_args()
    env = simpy.Environment()

    medium_name = "const_rate"
    
    t = TransmissionMedium(env, medium_name)
    # setting up logger    
    logger = logging.getLogger(medium_name)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(TraceFormatter(env))
    logger.addHandler(ch)
    t.add_logger(logger)

    total_time = args.sim_time
    use_seed = args.use_seed
    num_nodes = args.num_nodes
    protocol_type = args.type
    
    bs = create_basestation(protocol_type, 0, env, "default.json")
    t.add_device(bs)
    nodes_list = []

    for i in range(num_nodes):
        special_arg = {"total": num_nodes, "scheduled_time": i, "seed": i}
        n = create_node(protocol_type, i, env, "default.json", special_arg)
        nodes_list.append(n)
        t.add_device(n)

    env.process(sending(nodes_list, args.packet_rate, env))

    env.run(until=total_time)

if __name__ == "__main__":
    main()
