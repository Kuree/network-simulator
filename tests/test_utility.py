from pyns.utility import RandomMock

def test_mock():
    lst = list(range(10))
    r = RandomMock(lst)
    for i in lst:
        assert r.randrange(10) == i
    # test for different range
    for i in range(10):
        v = r.randrange(5)
        assert v == (i % 5)

    assert r.randint(2, 7) == 2
