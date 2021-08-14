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

BASE_CTRL = BaseCtrl()
tourneys_view = TourneysView()
player_view = PlayerView()
digest_view = DigestView()
rating_view = RatingView()

TOURNEYS_CTRL = TourneysCtrl(tourneys_view, BASE_CTRL)
PLAYER_CTRL = PlayerCtrl(player_view, BASE_CTRL)
DIGEST_CTRL = DigestCtrl(digest_view, BASE_CTRL)
RATING_CTRL = RatingCtrl(rating_view, BASE_CTRL)

new_tourney = {
    'name': "chessmanager",
    'at_date': "default",
    'at_place': "cherbourg",
    'turns': 'default',
    'time_handler': 'default'
}

tourney_index = BASE_CTRL.add_tourney()
tourney = BASE_CTRL.get_tourney_by_index(tourney_index)
for field in new_tourney:
    if field != "default":
        value = new_tourney[field]
    else:
        value = BASE_CTRL.get_field(filed)['default']

    tourney.set_field_value(field, value)
tourney.load()

new_player = {
    'first_name': "Sébastien",
    'last_name': "Larcher",
    'at_date': "11/06/1990"
}

new_player1 = {
    'first_name': "Zion",
    'last_name': "Hight",
    'at_date': "11/06/1990"
}

player_index = BASE_CTRL.add_player()
player1_index = BASE_CTRL.add_player()
player = BASE_CTRL.get_player_by_index(player_index)
player1 = BASE_CTRL.get_player_by_index(player1_index)
for field in new_player:
    if field != "default":
        value = new_player[field]
        value1 = new_player1[field]
    else:
        value = BASE_CTRL.get_field(field)['default']
        value1 = BASE_CTRL.get_field(field)['default']

    player.set_field_value(field, value)
    player1.set_field_value(field, value1)
player.load()

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
