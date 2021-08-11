from chester.models.player import Player
from chester.models.tourney import Tourney

class BaseCtrl:
    def __init__(self):
        self.available_players = []
        self.available_tourney = []
    
    def add_player(self):

        player = Player()
        self.available_players.append(player)
        return self.available_players.index(player)
    
    def get_player_by_index(self, index):

        return self.available_players[index]

    def get_all_players(self):

        return self.available_players

    def add_tourney(self):

        tourney = Tourney()
        self.available_tourney.append(tourney)

        return self.available_tourney.index(tourney)

    def get_tourney_by_index(self, index):

        return self.available_tourney[index]

    def get_all_tourney(self):

        return self.available_tourney
