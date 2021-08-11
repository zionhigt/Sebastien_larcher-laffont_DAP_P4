from chester.models.schemas.schema import Schema

from datetime import date

class Tourney(Schema):
    def __init__(self):
        config = {
                'name': {'required': True},
                'at_date': {'default': date.today().strftime("%d/%m/20%y")},
                'at_place': {'required': True},
                'turns': {'required': True, 'default': "4"},
                'time_handler': {'required': True, 'default': "bullet"},
                'comment': {}
            }
        super().__init__(config)

        self.rounds = []
        self.players = []

    def add_player(self, id):
        try:
            is_in_array = self.players.index(id)
            return is_in_array
        except ValueError:
            self.players.append(id)
            self.add_player(id)

if __name__ == '__main__':

    print("self.get():\n\t" + Tourney.get.__doc__)
