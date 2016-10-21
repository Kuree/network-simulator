import simpy
import random
import time

class Node(Device):
    def __init__(self, node_id, env):
        ''' 
            set up the basic variables used in the simulation
            sleep_time: used for every communication cycle of the node. nodes are responsible for updating the sleep time
        '''
        super.__init__(node_id)
        self.env = env
        self.random = random.Random() # unique seed
       
        # set up sleep time
        # by default it is active
        self.__sleep_time = 0

        self.action = env.process(self.run())

    def receive(self, size, rate = 1):
        ''' 
            this is used to recieve size from the master node at given rate
        '''
        return None


    def on_receive(self, packet):
        ''' receive message from the medium
        '''
        pass

    def send(self, packet, rate = 1):
        ''' this is used to send a packet to master node.
            packet has to be in bytes object
        '''
        pass

    def take_action(self, message):
        '''
           this is called after wake up
        '''
        pass

    def _get_time(self):
        return self.env.now

    def _update_sleep_time(self, time):
        ''' override this if you want the node to have a different sleep time
        '''
        pass


    def sleep_until(self, time):
        self.__sleep_time = time

    def listen(self, period = 5):
        ''' used when the node want for a period of time 
            to see if there is any ongoing traffic in the air.
            return True/False
        '''
        return False

    def run(self):
        ''' 
            this is used in any simulation. this simulation is designed for any slotted protocol.
            For scheduling purpose, an event is fired at each timeslot. the node can choose 
            how to react (continue to sleep or send a packet)
        '''
        while True:
            yield self.env.timeout(self.__sleep_time)
            self.__sleep_time = 0 # it won't sleep anymore untill you force it to in the take action
            self.take_action(self._message)
