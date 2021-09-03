from datetime import datetime


class Round:
    def __init__(self, name, tournament):
        self.name = name
        self.tournament = tournament
        self.players = []
        self.orphan_player = None
        self.meeting = []
        self.matchs = []
        self.state = "PROCESS"
        self.start_at = datetime.now()
        self.end_at = ""

    def mark_as_done(self):
        self.orphan_player = None
        self.state = 'DONE'
        self.end_at = datetime.now()
