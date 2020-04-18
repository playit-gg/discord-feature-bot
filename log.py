
from datetime import datetime

class Log(object):
    violations = 0
    lastMessage = datetime.now()

    def __init__(self, lastMessage):
        self.lastMessage = lastMessage