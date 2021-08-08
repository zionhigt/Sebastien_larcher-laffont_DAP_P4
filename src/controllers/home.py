from src.models.tourney import Tourney
from src.views.tourney import TourneyView

from .base import BaseCtrl
from .tourney import TourneyCtrl

from termcolor import colored as _c

BASE_CTRL = BaseCtrl()
tourney_view = TourneyView()
TOURNEY_CTRL = TourneyCtrl(tourney_view, BASE_CTRL)

class HomeCtrl:
    def __init__(self, view, tourney_view):
        self.view = view
        self.current_tourney_index = None
    
    def run(self):
        tourney_index = self.view.ask_for_load_tourney(BASE_CTRL.get_all_tourney())
        if tourney_index != "c":
            #TOURNEY_CTRL.load_tourney(int(tourney_index))
            self.current_tourney_index = int(tourney_index)
        else:
            new_tourney = self.tourney_maker()
            print(BASE_CTRL.get_tourney_by_index(new_tourney).get_schema_input())
            is_tourney_to_load = self.view.ask(f"Charger ce tournoi [{_c('O', 'green')}/{_c('N', 'red')}]")
            if is_tourney_to_load == "O":
                self.current_tourney_index = new_tourney

            elif is_tourney_to_load == 'N':
                self.run()

        if self.current_tourney_index is not None:
            TOURNEY_CTRL.load_tourney(self.current_tourney_index)
            print(self.current_tourney_index)

    def tourney_maker(self):
        added_tourney = BASE_CTRL.add_tourney() #return index of global list
        tourney = BASE_CTRL.get_tourney_by_index(added_tourney)
        self.view.asking_for_model(tourney)

        return added_tourney