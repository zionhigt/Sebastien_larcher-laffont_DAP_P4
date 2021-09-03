from chessmanager.models.schemas.schema import Schema
from datetime import date


class Player(Schema):
    def __init__(self):
        config = {
                'first_name': {'required': True},
                'last_name': {'required': True},
                'birth_date': {'required': True, 'type': date}
            }
        super().__init__(config)

        self.rating = 0
