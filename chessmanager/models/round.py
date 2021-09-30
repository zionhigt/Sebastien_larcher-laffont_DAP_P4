from datetime import datetime


class Round:
    def __init__(self, name, tournament):
        self.name = name
        self.tournament = tournament
        self.players = []
        self.matchs = []
        self.state = "PROCESS"
        self.start_at = datetime.now()
        self.end_at = ""

    def mark_as_done(self):
        self.state = 'DONE'
        self.end_at = datetime.now()

    def serialize(self, matchs):
        end_at = ""
        if self.end_at != "":
            end_at = self.end_at.timestamp()

        return {
            "name": self.name,
            "matchs": matchs,
            "start_at": self.start_at.timestamp(),
            "end_at": end_at,
            "state": self.state
        }
