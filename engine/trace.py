import logging

class TraceFormatter(logging.Formatter):
    def __init__(self, env):
        super.__init__()
        selv.env = env


    def format(self, record):
        id = record.id
        size    = record.size
        valid = 1 if not record.is_corrupted else 0
        return "{0} {1} {2} {3}".format(self.env.now, id, size, valid)
