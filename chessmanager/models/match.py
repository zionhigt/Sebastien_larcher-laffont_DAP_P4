from chessmanager.models.schemas.schema import Schema
from random import randint


from chessmanager.models.schemas.schema import Schema
from tinydb import where


class Match(Schema):
    def __init__(self, player_s1, player_s2):
        self.player_s1 = player_s1[0]
        self.player_s2 = player_s2[0]
        self.players = [self.player_s1, self.player_s2]
        self.colors = ["white", "black"]
        self.get_random_colors()
        self.score_s1 = 0.0
        self.score_s2 = 0.0
        self.played = False
        query_match = lambda x=None: (where('player_s1') == self.player_s1 & where('player_s1') == self.player_s1)
        super().__init__(None, 'Matchs', query_match)

    def add_points(self, scores):

        self.score_s1 += scores[0]
        self.score_s2 += scores[1]

    def get_random_colors(self):
        white_place = randint(0, 1)
        black_place = int(not white_place)
        self.colors[white_place] = "white"
        self.colors[black_place] = "black"
