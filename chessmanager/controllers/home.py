from chessmanager.controllers.base import BaseCtrl
from chessmanager.controllers.ctrl import Ctrl

from chessmanager.views.tourneys import TourneysView
from chessmanager.controllers.tourneys import TourneysCtrl

from chessmanager.views.player import PlayerView
from chessmanager.controllers.player import PlayerCtrl

from chessmanager.views.digest import DigestView
from chessmanager.controllers.digest import DigestCtrl

from chessmanager.views.rating import RatingView
from chessmanager.controllers.rating import RatingCtrl

from termcolor import colored as _c

import json

from random import randint

BASE_CTRL = BaseCtrl()
tourneys_view = TourneysView()
player_view = PlayerView()
digest_view = DigestView()
rating_view = RatingView()

TOURNEYS_CTRL = TourneysCtrl(tourneys_view, BASE_CTRL)
PLAYER_CTRL = PlayerCtrl(player_view, BASE_CTRL)
DIGEST_CTRL = DigestCtrl(digest_view, BASE_CTRL)
RATING_CTRL = RatingCtrl(rating_view, BASE_CTRL)

def makeItems(model, config):
    for field in config:
        if config[field] != "default":
            value = config[field]
        else:
            value = model.get_field(field)['default']
        model.set_field_value(field, value)
    model.load()


new_tourney = {
    'name': "chessmanager",
    'at_date': "default",
    'at_place': "cherbourg",
    'turns': "default",
    'time_handler': "default"
}

tourney_index = BASE_CTRL.add_tourney()
tourney = BASE_CTRL.get_tourney_by_index(tourney_index)
makeItems(tourney, new_tourney)

with open("./data/json/players.json", 'r') as players_file:
    players = json.load(players_file)
    for player_config in players:
        player_index = BASE_CTRL.add_player()
        player = BASE_CTRL.get_player_by_index(player_index)
        makeItems(player, player_config)
        score_player = randint(0, 15)
        player.add_point(score_player)

    players_file.close()

class HomeCtrl(Ctrl):
    def __init__(self, view):
        self.view = view
        self.base_actions = [
            ('Gestion des tournois', False, 'run_tourney'),
            ('Gestion des Joueurs', False, 'run_player'),
            ('Rapports', False, 'run_digest'),
            ('Mise à jour des classements', False, 'run_rating'),
        ]
        self.actions_callbacks = {
            'run_tourney': TOURNEYS_CTRL.run,
            'run_player': PLAYER_CTRL.run,
            'run_digest': DIGEST_CTRL.run,
            'run_rating': RATING_CTRL.run
        }

    def show_available_actions(self):
        """Provide an actions handler for users navigation"""

        self.show_actions(self.base_actions, self.actions_callbacks)
        self.show_available_actions()

    def run(self):
        self.show_available_actions()
