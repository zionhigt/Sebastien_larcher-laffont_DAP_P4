from chessmanager.controllers.base import BaseCtrl
from chessmanager.controllers.ctrl import Ctrl

from chessmanager.views.tournaments import TournamentsView
from chessmanager.controllers.tournaments import TournamentsCtrl

from chessmanager.views.player import PlayerView
from chessmanager.controllers.player import PlayerCtrl

from chessmanager.views.rating import RatingView
from chessmanager.controllers.rating import RatingCtrl


BASE_CTRL = BaseCtrl()
tournaments_view = TournamentsView("Chessmanager>Tournois>")
player_view = PlayerView("Chessmanager>Joueurs>")
rating_view = RatingView("Chessmanager>Classement>")

tournaments_CTRL = TournamentsCtrl(tournaments_view, BASE_CTRL)
PLAYER_CTRL = PlayerCtrl(player_view, BASE_CTRL)
RATING_CTRL = RatingCtrl(rating_view, BASE_CTRL)


class HomeCtrl(Ctrl):
    def __init__(self, view):
        super().__init__(view)

        # (wording, hidden, callback_name)
        self.base_actions = [
            ('Gérer les tournois', False, 'run_tournament'),
            ('Gérer les Joueurs', False, 'run_player'),
            ('Sauvgarder la partie', False, 'save'),
            ('Charger la partie', False, 'load'),
            ('Éditer les classements', False, 'run_rating'),
        ]
        self.actions_callbacks = {
            'run_tournament': tournaments_CTRL.run,
            'run_player': PLAYER_CTRL.run,
            'save': BASE_CTRL.save,
            'load': BASE_CTRL.load,
            'run_rating': RATING_CTRL.run
        }

    def show_available_actions(self):
        """Provide an actions handler for users navigation"""
        self.show_actions(self.base_actions, self.actions_callbacks)
        self.show_available_actions()

    def run(self):
        self.show_available_actions()
