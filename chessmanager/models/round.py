from datetime import datetime


class Round:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.meeting = []
        self.matchs = []
        self.state = "PROCESS"
        self.start_at = datetime.now()
        self.end_at = ""
    
    def mark_as_done(self):
        self.state = 'DONE'
        self.end_at = datetime.now()