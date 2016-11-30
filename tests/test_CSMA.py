from bootstrap import *

from engine import TransmissionMedium
from protocols import CSMANode, CSMABaseStation
import simpy

def test(env, nodes, bs):
    def on_receive5(*args):
        assert abs(env.now - 1) < 0.1
    bs.on_receive = on_receive5
    nodes[0].send("test", nodes[0].MTU)
    yield env.timeout(3)
    
    # simulation time now is 3
    def on_receive2(*args):
        assert abs(env.now - 4) < 0.1
    bs.on_receive = on_receive2
    
    nodes[2].send("test", nodes[2].MTU)
    yield env.timeout(0.8)
    
    nodes[1].send("test", nodes[1].MTU)
    def on_receive3(*args):
        assert abs(env.now - 5) < 0.1
    yield env.timeout(0.5)
    bs.on_receive = on_receive3
    yield env.timeout(20)


def main():
    env = simpy.Environment()
    rates = [30]
    t = TransmissionMedium(env)
    bs = CSMABaseStation(0, env, rates)
    t.add_device(bs)
    nodes = []
    TOTAL = 3
    for i in range(1, TOTAL + 1):
        node = CSMANode(i, env, rates, 0.5, guard = 0.01, seed = i, jitter_range = 0.001)
        t.add_device(node)
        nodes.append(node)
    env.process(test(env, nodes, bs))
    
    env.run(until=40)

if __name__ == "__main__":
    main()
