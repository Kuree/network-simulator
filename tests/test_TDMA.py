from bootstrap import *

from engine import TransmissionMedium
from protocols import TDMANode, TDMABaseStation
import simpy

def test(env, nodes, bs):
    def on_receive5(*args):
        assert abs(env.now - 6) < 0.1
    bs.on_receive += on_receive5
    nodes[5].send("test", nodes[5].MTU)
    yield env.timeout(10)
    
    # simulation time now is 10
    def on_receive2(*args):
        assert abs(env.now - 23) < 0.1
    yield env.timeout(3)
    bs.on_receive -= on_receive5
    bs.on_receive += on_receive2
    nodes[2].send("test", nodes[2].MTU)
    yield env.timeout(15)


def main():
    env = simpy.Environment()
    rates = [30]
    t = TransmissionMedium(env)
    bs = TDMABaseStation(0, env, rates)
    t.add_device(bs)
    nodes = []
    TOTAL = 10
    for i in range(1, TOTAL + 1):
        node = TDMANode(i, i-1, TOTAL, env, rates, guard = 0.01, seed = i, jitter_range = 0.001)
        t.add_device(node)
        nodes.append(node)
    env.process(test(env, nodes, bs))
    
    env.run(until=30)

if __name__ == "__main__":
    main()
