from chessmanager.models.schemas.schema import Schema

from datetime import date

class Tourney(Schema):
    def __init__(self):
        config = {
                'name': {'required': True},
                'at_date': {'required': True, 'default': date.today().__str__(), 'type': date},
                'at_place': {'required': True},
                'turns': {'required': True, 'default': 4, 'type': int},
                'time_handler': {'required': True, 'default': "bullet"},
                'comment': {}
            }
        super().__init__(config)

        self.rounds = []
        self.players = []

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
            is_in_array = self.players.index(player)
            return self.players[is_in_array]
        except ValueError:
            self.players.append(player)
            self.add_player(player)

if __name__ == '__main__':

    print("self.get():\n\t" + Tourney.get.__doc__)
