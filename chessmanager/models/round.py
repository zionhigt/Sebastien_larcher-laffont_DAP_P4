from datetime import datetime

from chessmanager.models.schemas.schema import Schema
from tinydb import where


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
        query_round = lambda x=None: (where('name') == self.name & where('tournament') == self.tournament)
        super().__init__(None, 'Matchs', query_round)

    def mark_as_done(self):
        self.orphan_player = None
        self.state = 'DONE'
        self.end_at = datetime.now()
