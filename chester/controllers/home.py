from chester.controllers.base import BaseCtrl

from chester.views.tourney import TourneyView
from chester.controllers.tourney import TourneyCtrl

from chester.views.player import PlayerView
from chester.controllers.player import PlayerCtrl

from chester.views.digest import DigestView
from chester.controllers.digest import DigestCtrl

from chester.views.rating import RatingView
from chester.controllers.rating import RatingCtrl

from termcolor import colored as _c

BASE_CTRL = BaseCtrl()
tourney_view = TourneyView()
player_view = PlayerView()
digest_view = DigestView()
rating_view = RatingView()

TOURNEY_CTRL = TourneyCtrl(tourney_view, BASE_CTRL)
PLAYER_CTRL = PlayerCtrl(player_view, BASE_CTRL)
DIGEST_CTRL = DigestCtrl(digest_view, BASE_CTRL)
RATING_CTRL = RatingCtrl(rating_view, BASE_CTRL)

new_tourney = {
    'name': "chester",
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

player_index = BASE_CTRL.add_player()
player = BASE_CTRL.get_player_by_index(player_index)
for field in new_player:
    if field != "default":
        value = new_player[field]
    else:
        value = BASE_CTRL.get_field(filed)['default']

    player.set_field_value(field, value)
player.load()

class HomeCtrl:
    def __init__(self, view):
        self.view = view

        self.base_actions = [
            ('Gestion des tournois', False, 'run_tourney'),
            ('Gestion des Joueurs', False, 'run_player'),
            ('Rapports', False, 'run_digest'),
            ('Mise à jour des classements', False, 'run_rating'),
        ]

        self.actions_callbacks = {
            'run_tourney': TOURNEY_CTRL.run,
            'run_player': PLAYER_CTRL.run,
            'run_digest': DIGEST_CTRL.run,
            'run_rating': RATING_CTRL.run
        }

    def show_actions(self):
        user_choice = self.view.show(self.base_actions)
        callback_name = self.base_actions[int(user_choice)][2]
        callback_methode = self.actions_callbacks[callback_name]
        callback_methode()
        self.show_actions()

    def run(self):
        self.show_actions()
