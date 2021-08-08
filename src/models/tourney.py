from datetime import date
from .schemas.schema import Schema

class Tourney(Schema):
    def __init__(self):
        config = {
                'name': {'required': True},
                'at_date': {'value': date.today()},
                'at_place': {},
                'turns': {'required': True, 'value': "4"},
                'time_handler': {'required': True, 'value': "bullet"},
                'comment': {}
            }
        super().__init__(config)

        self.rounds = []
        self.players = []

if __name__ == '__main__':

    print("self.get():\n\t" + Tourney.get.__doc__)
