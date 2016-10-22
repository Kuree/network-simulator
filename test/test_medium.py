if __name__ == '__main__' and __package__ is None:
   from os import sys, path
   sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from engine import TransmissionMedium
import simpy
from engine import Device

if __name__ == "__main__":
    def r(obj):
        print(obj.id, obj.payload)

    env = simpy.Environment()

    def test():
        while True:
            t = TransmissionMedium(env)
            env.process(t.run())
            d = Device(1)
            d.on_receive = r
            t.add_device(d)
            d._send("yo", 1)
            yield env.timeout(1)
            print(t.is_busy())
            d.sleep()
            d._send("sup", 1)
            print(t.is_busy())
            yield env.timeout(1)
            print(t.is_busy())
            break
    env.process(test())
    env.run(until=5)

