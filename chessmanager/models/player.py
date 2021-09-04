from chessmanager.models.schemas.schema import Schema
from datetime import date
from tinydb import where


class Player(Schema):
    def __init__(self):
        config = {
                'first_name': {'required': True},
                'last_name': {'required': True},
                'birth_date': {'required': True, 'type': date}
            }
        query_player = lambda x=None: ((where('last_name') == self.to_dict()['last_name']) &
        (where('first_name') == self.to_dict()['first_name']) &
        (where('birth_date') == self.to_dict()['birth_date']))
        super().__init__(config, 'Player', query_player)

        self.rating = 0
