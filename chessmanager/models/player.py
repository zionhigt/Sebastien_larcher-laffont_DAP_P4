from chessmanager.models.schemas.schema import Schema
from datetime import date

class Player(Schema):
    def __init__(self):
        config = {
                'first_name': {'required': True},
                'last_name': {'required': True},
                'at_date': {'default': date.today().strftime("%d/%m/20%y")},
            }
        super().__init__(config)

        self.score = 0
    
    def get_score(self):
        return self.score
    
    def add_point(self, point):
        self.score += point
        return self.score
    
