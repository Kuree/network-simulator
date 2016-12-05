import math
from pyns.engine import Device

class DQNObject:
    REQUEST = 0
    FEEDBACK = 1
    def __init__(self, obj_type):
        self.type = obj_type


class DQNRequest(DQNObject):
    def __init__(self, slots):
        # NOTE: this is used as how many data slots the node requests
        super().__init__(DQObject.REQUEST)
        self.slots = slots

class DQNFeedback(DQNObject):
    def __init__(self, slots, data_count, dtq, crq):
        self.slots = slots
        self.data_count
        self.dtq = dtq
        self.crq = crq


class DQNNode(Device):
    # finite state machine
    IDLE = 0
    IN_TRANSMISSION = 1
    DTQ  = 2
    CRQ  = 3
    WAIT = 4

    def __init__(self, id, env, N, seed, jitter_range, rates, m, slot_t, feedback_t, guard):
        MTU = self._compute_mtu((1 - guard) * N, rates[0])
        super().__init__(id, env, rates, seed=seed, jitter_range=jitter_range, guard=guard, MTU = MTU)
        #self.average_packet_size = average_packet_size
        self.m = m
        self.N = N
        # this controls the time for overhead
        self.slot_t = slot_t
        self.feedback_t = feedback_t

        # smooth out the start up process
        self.sleep_time = 0
        
        self.chosen_slot = 0
        
        self.state = DQNNode.IDLE

        self.on_receive += self.__node_on_receive

    def __node_on_receive(self, packet):
        if self.state == DQNNode.WAIT:
            payload = packet.payload
            if type(payload) != DQFeedback:
                return # not valid packet
            if payload.slots[self.chosen_slot][0] == 1: # it's a successful request
                queue_position = 0
                for i in range(self.chosen_slot):
                    if payload.slots[i][0] == 1:
                        queue_position += payload.slots[i][1] # compute the dtq
                raw_sleep_time = payload.dtq + queue_position
                self.sleep_time = raw_sleep_time + raw_sleep_time // self.N # take into account the overhead block
                self.state = DQNNode.DTQ
            elif payload.slots[self.chosen_slot] > 1:
                # enter crq
                queue_position = 0
                for i in range(self.chosen_slot):
                    if payload.slots[i][0] > 1:
                        queue_position += 1 # compute the crq position
                self.sleep_time = payload.crq + queue_position
                self.state = DQNNode.CRQ
            else:
                # TODO: this is packet loss
                raise Exception("time", self.env.now, "id", self.id, "chosen", self.chosen_slot)


    def _schedule_send(self, payload, duration, size, medium_index, is_overhead, antenna):
        with antenna.request() as req:
            yield req
            self.state = DQNNode.IN_TRANSMISSION
            self.sleep_time = (1 - (self.env.now % 1)) % 1
            while self.should_send:
                yield self.env.timeout(self.sleep_time)
                if self.state == DQNNode.IN_TRANSMISSION:
                    # sleep 
                    self.chosen_slot = self.random.randrange(self.m)
                    # compute the offset for slot
                    # sleep_time
                    sleep_time = self.slot_t / self.m * self.chosen_slot
                    yield self.env.timeout(sleep_time)
                    slot_duration = self.slot_t / self.m - self.guard
                    slot_size = slot_duration * self.rates[0]
                    num_of_data_slots = math.ceil(size / (self.MTU / self.N))
                    self._send(DQRequest(self.chosen_slot, num_of_data_slots), slot_duration, slot_size, 0, is_overhead = True)

                    # this will put it to sleep till contention result is out
                    self.state = DQNNode.WAIT
                    yield self.env.timeout(1 - (self.env.now % 1))
                    
                elif self.state == DQNNode.DTQ:
                    # skip the slot time
                    yield self.env.timeout(self.slot_t)
                    # TODO: fix the rate here
                    self._send(payload, duration = duration, size=size, medium_index = 0, is_overhead = False)
                    self.state = DQNNode.IDLE
                    self.should_send = False
                elif self.state == DQNNode.CRQ:
                    # try to transmit again
                    self.sleep_time = (1 - (self.env.now % 1)) % 1
                    self.state = DQNNode.IN_TRANSMISSION


class DQNBaseStation(Device):
    def __init__(self, id, env, N, seed, m, rates, jitter_range, feedback_t, slot_t):
        super().__init__(id, env, rates, seed = seed, jitter_range = jitter_range)
        self.m = m
        self.N = N
        self.feedback_t = feedback_t
        self.slot_t = slot_t
        
        self.window_size = 0.01 # 0.1 buffer
        self.dtq = 0
        self.crq = 0

        self.__init_slots()
        self.on_receive += self.__bs_on_receive

        self.env.process(self.run())


    def __bs_on_receive(self, packet):
        payload = packet.payload
        if type(payload) == DQNRequest:
            # only interested in slot request
            slot_raw = self.env.now % 1 # TODO: calibrate with the receive window
            if slot_raw < 0:
                slot_raw = 0
            slot = int(slot_raw / self.slot_t * self.m)
            if slot < self.m: # if it's larger or equal to, we don't need to take care of as it will cause packet drop
                self.slots[slot][1] += payload.slots
                self.slots[slot][0] += 1
       
    def __compute_slot(self, time):
        raw_slot = time / self.slot_t * self.m
        # notice that simple int() won't work
        for i in range(self.m):
            if abs(raw_slot - i) < self.jitter_range * 2:
                return i
        raise Exception("received at wrong time!")

    def _on_collision(self):
        time = self.env.now % 1
        if time < self.slot_t: # collision in the request slot
            slot = self.__compute_slot(time)
            if slot < self.m:
                if self.slots[slot][0] == 0:
                    self.slots[slot][0] += 2
                else:
                    self.slots[slot][0] += 1

    def __init_slots(self):
        self.slots = [[0, 0] for i in range(self.m)]


    def run(self):
        # dump to feedback slot
        yield self.env.timeout(1 - self.slot_t)
        while True:
            duration =  self.feedback_t - self.window_size
            size = self.rates[0] * duration
            self._send(DQFeedback(self.slots, self.dtq, self.crq), duration, size, medium_index = 0, is_overhead = True)

            # increment the counter accordingly
            for i in range(len(self.slots)):
                if self.slots[i][0] > 1:
                    self.crq += 1
                elif self.slots[i][0] == 1:
                    self.dtq += self.slots[i][1]

            self.__init_slots()
            yield self.env.timeout(1)
            # decrease the counter
            self.dtq = self.dtq - N if self.dtq > N else 0
            self.crq = self.crq - 1 if self.crq > 0 else 0
        



