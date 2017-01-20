from pyns.engine import Device


'''
This implements a simplified LORAWAN class A
'''


class LORAACK:
    def __init__(self):
        pass

class LORANode(Device):
    def __init__(self, id, env, rates,  seed, jitter_range, guard):
        MTU = rates[0] * (1 - guard * 2)
        super().__init__(id, env, rates, seed=seed, jitter_range=jitter_range, guard=guard, MTU = MTU)


    def create_receive_window(self):
        def received_window(packet):
            payload = packet.payload
            if type(payload) == LORAACK:
                self.should_send = False
        return received_window


    def _schedule_send(self, payload, duration, size, medium_index, is_overhead, antenna):
        with antenna.request() as req:
            yield req
            while self.should_send:
                self._send(payload, duration, size, medium_index, is_overhead)
                yield self.env.timeout(duration) # wait till the transmission is finished
                # TODO: fixed the time using the real time
                # now each unit time is 0.2 second so it will wati for 5 unit of time
                yield self.env.timeout(5)
                receive1 = self.create_receive_window()
                self.on_receive += receive1
                yield self.env.timeout(1) # actually it will use a very short of time (0.1 unit)
                # finished receiving
                self.on_receive -= receive1
                if self.should_send:
                    yield self.env.timeout(4)
                    # add the receive window
                    self.on_receive += receive1
                    # another receive window
                    yield self.env.timeout(1)
                    # finish it up
                    self.on_receive -= receive1

class LORABaseStation(Device):
    def __init__(self, id, env, rates):
        super().__init__(id, env, rates)
        self.on_signal += Device._invalidate_packet_receive(self)

        self.on_receive += self.lora_receive

    def receive_window(self):
        # wait for 1 sec
        yield self.env.timeout(5)
        size = 1
        self.send(LORAACK(), size)

    def lora_receive(self, packet):
        # always choose the first receive wintow
        self.env.process(self.receive_window())
