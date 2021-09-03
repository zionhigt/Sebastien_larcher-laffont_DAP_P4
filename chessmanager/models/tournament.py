from chessmanager.models.schemas.schema import Schema
from chessmanager.models.schemas.type import time_handler

from datetime import date


class Tournament(Schema):
    def __init__(self):
        config = {
                'name': {'required': True},
                'at_date': {'required': True, 'default': date.today().__str__(), 'type': date},
                'at_place': {'required': True},
                'turns': {'required': True, 'default': 4, 'type': int},
                'time_handler': {'required': True, 'default': "bullet", 'type': time_handler},
                'comment': {}
            }
        super().__init__(config)

        self.rounds = []

        # [(class Player, score)]
        self.players = []

        self.state = "AWAIT"
        self.started = False
        self.ended = False

    def get_tournament_player(self, player):
        tournament_players = [player[0] for player in self.players]
        player_index = tournament_players.index(player)
        return self.players[player_index]

    def update_player_set_score(self, player, point):
        player = self.get_tournament_player(player)
        player_index = self.players.index(player)
        self.players[player_index][1] = point

    def update_players_scores(self):
        all_matchs = [match for t_round in self.rounds for match in t_round.matchs]
        matchs_players = [match.players for match in all_matchs]
        scores_sections = [[match.score_s1, match.score_s2] for match in all_matchs]
        for player in self.players:
            tournament_player_score = 0
            for players_index in range(len(matchs_players)):
                players = matchs_players[players_index]
                if player[0] in players:
                    player_section = players.index(player[0])
                    tournament_player_score += scores_sections[players_index][player_section]
            self.update_player_set_score(player[0], tournament_player_score)

    def add_players(self, players):
        added_players = []
        for player in players:
            self.add_player(player)
            added_players.append(player)
        return added_players

    def add_player(self, player):
        if player is list:
            return self.add_players(player)
        try:
            all_players = [player[0] for player in self.players]
            index_in_array = all_players.index(player)
            return self.players[index_in_array]
        except ValueError:
            self.players.append([player, 0.0])
            self.add_player(player)

    def add_round(self, t_round):
        try:
            is_in_array = self.rounds.index(t_round)
            return self.rounds[is_in_array]
        except ValueError:
            self.rounds.append(t_round)
            self.add_round(t_round)
