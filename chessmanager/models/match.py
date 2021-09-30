from random import randint


class Match:
    def __init__(self, player_s1, player_s2):
        self.player_s1 = player_s1[0]
        self.player_s2 = player_s2[0]
        self.players = [self.player_s1, self.player_s2]
        self.colors = ["white", "black"]
        self.get_random_colors()
        self.score_s1 = 0.0
        self.score_s2 = 0.0
        self.played = False

    def add_points(self, scores):

        self.score_s1 += scores[0]
        self.score_s2 += scores[1]

    def get_random_colors(self):
        white_place = randint(0, 1)
        black_place = int(not white_place)
        self.colors[white_place] = "white"
        self.colors[black_place] = "black"

    def serialize(self):
        return {
            "player_s1": self.available_players.index(self.player_s1),
            "player_s2": self.available_players.index(self.player_s2),
            "score_s1": self.score_s1,
            "score_s2": self.score_s2,
            "colors_s1": self.colors[0],
            "colors_s2": self.colors[1],
            "played": self.played
        }
