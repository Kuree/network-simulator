import logging

class TraceFormatter(logging.Formatter):
    def __init__(self, env):
        self.env = env
        super(TraceFormatter, self).__init__()

    def format(self, record):
        packet = record.msg
        id = packet.id
        size    = packet.size
        valid = 1 if not packet.is_corrupted else 0
        return "{0} {1} {2} {3}".format(self.env.now, id, size, valid)
