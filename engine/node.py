import simpy
import random
import time

class Node(Device):
    def __init__(self, node_id, env, initial_sleep_time = 0):
        ''' 
            set up the basic variables used in the simulation
            sleep_time: used for every communication cycle of the node. nodes are responsible for updating the sleep time
        '''
        super.__init__(node_id)
        self.env = env
        self.random = random.Random() # unique seed
       
        # set up sleep time
        # by default it is active
        # set the initial_sleep_time to a different number so that the simulation will have a smooth start
        self.__sleep_time = initial_sleep_time

        self.action = env.process(self.run())

    def on_receive(self, packet):
        ''' invoked when a message is received.
            this one can be used to wake up the node upon receiving certain message
        '''
        pass

    def send(self, payload, duration = 1):
        ''' this is used to send a packet to master node.
            packet has to be in bytes object
        '''
        self._send(payload, duration)

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
            this is used in any simulation. this simulation is designed for.
            For scheduling purpose, an event is fired at each timeslot. the node can choose 
            how to react (continue to sleep or send a packet)
        '''
        while True:
            if self.__sleep_time > 0:
                self.sleep()
                yield self.env.timeout(self.__sleep_time)
                self.take_action()
            else:
                # 0.001 is the simulation precision
                yield self.env.timeout(0.001)
