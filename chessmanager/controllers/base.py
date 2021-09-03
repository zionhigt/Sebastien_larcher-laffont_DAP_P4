from chessmanager.models.player import Player
from chessmanager.models.tournament import Tournament


class BaseCtrl:
    def __init__(self):
        self.available_players = []
        self.available_tournament = []

    def add_player(self):

        player = Player()
        self.available_players.append(player)
        player.rating = len(self.available_players)
        return self.available_players.index(player)

    def get_player_by_index(self, index):

        return self.available_players[index]

    def delete_player_by_index(self, index):
        if len(self.available_players) > index:
            del self.available_players[index]

    def get_all_players(self):

        return self.available_players

    def add_tournament(self):

        tournament = Tournament()
        self.available_tournament.append(tournament)

        return self.available_tournament.index(tournament)

    def get_tournament_by_index(self, index):

        return self.available_tournament[index]

    def get_all_tournament(self):

        return self.available_tournament

    def delete_tournament_by_index(self, index):
        if len(self.available_tournament) > index:
            del self.available_tournament[index]
