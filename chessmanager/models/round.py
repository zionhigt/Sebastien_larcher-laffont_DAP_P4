from datetime import datetime

from chessmanager.models.schemas.schema import Schema
from tinydb import where


class Round(Schema):
    def __init__(self, name=None, tournament=None):
        self.name = name
        self.tournament = tournament
        self.players = []
        self.orphan_player = None
        self.matchs = []
        self.state = "PROCESS"
        self.start_at = datetime.now()
        self.end_at = ""
        query_round = lambda x=None: ((where('name') == self.to_dict()['name'])) # & (where('start_at') == self.to_dict()['start_at'])
        super().__init__(None, 'Rounds', query_round)

    def mark_as_done(self):
        self.state = 'DONE'
        self.end_at = datetime.now()
