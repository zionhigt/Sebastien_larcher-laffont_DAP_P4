from chessmanager.models.schemas.schema import Schema
from datetime import date

class Player(Schema):
    def __init__(self):
        config = {
                'first_name': {'required': True},
                'last_name': {'required': True},
                'at_date': {'required': True, 'type': date},
                'rating': {'default': 0, 'type': int}
            }
        super().__init__(config)

    
