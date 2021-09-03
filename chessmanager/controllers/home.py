from chessmanager.controllers.base import BaseCtrl
from chessmanager.controllers.ctrl import Ctrl

from chessmanager.views.tournaments import TournamentsView
from chessmanager.controllers.tournaments import TournamentsCtrl

from chessmanager.views.player import PlayerView
from chessmanager.controllers.player import PlayerCtrl

from chessmanager.views.rating import RatingView
from chessmanager.controllers.rating import RatingCtrl

import json


BASE_CTRL = BaseCtrl()
tournaments_view = TournamentsView("Chessmanager>Tournois>")
player_view = PlayerView("Chessmanager>Joueurs>")
rating_view = RatingView("Chessmanager>Classement>")

tournaments_CTRL = TournamentsCtrl(tournaments_view, BASE_CTRL)
PLAYER_CTRL = PlayerCtrl(player_view, BASE_CTRL)
RATING_CTRL = RatingCtrl(rating_view, BASE_CTRL)


def make_items(model, config):
    for field in config:
        if config[field] != "default":
            value = config[field]
        else:
            value = model.get_field(field)['default']
        model.set_field_value(field, value)
    model.load()


new_tournament = {
    'name': "chessmanager",
    'at_date': "default",
    'at_place': "cherbourg",
    'turns': "default",
    'time_handler': "default"
}

tournament_index = BASE_CTRL.add_tournament()
tournament = BASE_CTRL.get_tournament_by_index(tournament_index)
make_items(tournament, new_tournament)

with open("./data/json/players.json", 'r') as players_file:
    players = json.load(players_file)
    for player_config in players:
        player_index = BASE_CTRL.add_player()
        player = BASE_CTRL.get_player_by_index(player_index)
        make_items(player, player_config)
        tournament.add_player(player)

    players_file.close()


class HomeCtrl(Ctrl):
    def __init__(self, view):
        super().__init__(view)
        self.base_actions = [
            ('Gérer les tournois', False, 'run_tournament'),
            ('Gérer les Joueurs', False, 'run_player'),
            ('Éditer les classements', False, 'run_rating'),
        ]
        self.actions_callbacks = {
            'run_tournament': tournaments_CTRL.run,
            'run_player': PLAYER_CTRL.run,
            'run_rating': RATING_CTRL.run
        }

    def show_available_actions(self):
        """Provide an actions handler for users navigation"""

        self.show_actions(self.base_actions, self.actions_callbacks)
        self.show_available_actions()

    def run(self):
        self.show_available_actions()
