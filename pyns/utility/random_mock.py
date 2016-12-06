import itertools
import random

class RandomMock:
    def __init__(self, numbers):
        ''' a number generator'''
        self.it = itertools.cycle(numbers)
        self.it_max = max(numbers)

    def randint(self, a, b):
        next_random = next(self.it)
        return a + (next_random) % (b - a)

    def randrange(self, stop):
        next_random = next(self.it)
        return next_random % stop

    def random(self):
        # use the old one
        return random.random()

