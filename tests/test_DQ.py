from bootstrap import *

from engine import TransmissionMedium
from protocols import LPDQNode, LPDQBaseStation
import simpy
from random_mock import RandomMock

def test(env, nodes, bs):
    MTU = nodes[0].MTU
    def on_receive1(packet):
        payload = packet.payload
        print(payload)
        if type(payload) == str:
            print(env.now)
            # first node should not have any problem
            assert abs(env.now - 2) < 0.1
    bs.on_receive += on_receive1
    nodes[0].send("test", MTU)
    yield env.timeout(3)

    # simulation time is 3 now
    #nodes[1].send("", MTU)
    #nodes[2].send("", MTU)
    def on_receive2(payload):
        if type(payload) != str:
            print(env.now)
            print(payload)
        else:
            print(env.now)
    #bs.on_receive = on_receive2
    yield env.timeout(5) 


def main():
    env = simpy.Environment()
    rates = [30]
    slot_t = 0.1
    feedback_t = 0.1

    random_list = range(10)

    t = TransmissionMedium(env)
    bs = LPDQBaseStation(0, env, 0, 3, rates=rates, jitter_range = 0.0001, feedback_t = feedback_t, slot_t = slot_t)
    bs.random = RandomMock(random_list)
    t.add_device(bs)
    nodes = []
    TOTAL = 10
    for i in range(1, TOTAL + 1):
        node = LPDQNode(i, env, feedback_t = feedback_t, slot_t = slot_t, m=3, rates = rates, guard = 0.01, seed = i, jitter_range = 0.001)
        t.add_device(node)
        nodes.append(node)
        node.random = RandomMock(random_list)
    env.process(test(env, nodes, bs))
    
    env.run(until=30)

if __name__ == "__main__":
    main()
