import itertools
class Random:
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



if __name__ == "__main__":
    lst = list(range(10))
    r = Random(lst)
    for i in lst:
        assert r.randrange(10) == i
    # test for different range
    for i in range(10):
        v = r.randrange(5)
        assert v == (i % 5)

    assert r.randint(2, 7) == 2
        
