from chessmanager.controllers.ctrl import Ctrl
from chessmanager.controllers.ctrl import compute_available_action

from chessmanager.views.tourney import TourneyView
from chessmanager.controllers.tourney import TourneyCtrl
from chessmanager.models.tourney import Tourney

from termcolor import colored as _c

class TourneysCtrl(Ctrl):
    def __init__(self, view, base_ctrl):
        self.view = view
        self.base_ctrl = base_ctrl
        self.tourney_ctrl = TourneyCtrl(TourneyView(), self.base_ctrl)

        # {text, hidden, callback}
        self.base_actions = [
            ('Créer un tournois', False, 'create_tourney'),
            ('Charger un tournoi', True, 'load_tourney'),
            ('Liste des tournois', True, 'show_tourneys'),
            ('Retour au menu principal', False, 'return'),
            ('Aide', False, 'show_helper')
        ]

        self.action_callback = {
            'create_tourney': self.create_tourney,
            'load_tourney': self.asking_for_load_tourneys,
            'show_tourneys': self.show_tourneys,
            'return': self.exit,
            'show_helper': self.show_helper
        }

    def show_helper(self):
        self.view.show_helper()
        self.show_available_actions()
        return
    
    @compute_available_action
    def actions_rules(self):
        """Define what field will be show when tourney will be unloaded"""

        base_actions = list(map(lambda x: list(x), self.base_actions))
        if len(self.base_ctrl.get_all_tourney()) != 0:
            base_actions[1][1] = False
            base_actions[2][1] = False
        
        return base_actions

    def show_available_actions(self):
        """Showing availables actions when no tourney has loaded
        """

        actions_available = self.actions_rules()
        self.show_actions(actions_available, self.action_callback)
        return 

    def asking_for_load_tourneys(self):
        """Asking user to load an available tourney
        """
        tourney_index = self.view.ask_for_load_tourney(self.base_ctrl.get_all_tourney())
        self.load_tourney(int(tourney_index))
        return

    def show_tourneys(self):
        """Showing availables tourney
        """

        self.view.show_tourneys_table(self.base_ctrl.get_all_tourney())
        self.show_available_actions()
        return


    def load_tourney(self, tourney_index):
        """Turn a tourney to load
        Arguments:
            tourney_index -- index of the tourney saved into the base controller 
        """

        tourney = self.base_ctrl.get_tourney_by_index(tourney_index)
        if tourney.load():
            # self.show_loaded_actions()
            self.tourney_ctrl.run(tourney)
            self.show_available_actions()
        else:
            print('Ce tournoi ne peux pas être chargé')
        return

    def create_tourney(self):
        """Asking user for tourney informations
        """
        new_tourney = self.tourney_maker()
        if new_tourney != False:
            is_tourney_to_load = self.view.ask(f"Charger ce tournoi {_c('[O/N]', 'grey', 'on_white')} ?")
            if is_tourney_to_load.upper() == "O":
                self.current_tourney_index = new_tourney
                self.load_tourney(new_tourney)

            elif is_tourney_to_load.upper() == 'N':
                self.show_available_actions()

        self.show_available_actions()
        return

    def run(self):
        self.show_available_actions()
        return

    def tourney_maker(self):
        # return index of global list
        new_tourney_index = self.base_ctrl.add_tourney()
        new_tourney = self.base_ctrl.get_tourney_by_index(new_tourney_index)
        if self.view.asking_for_model(new_tourney) != False:
            self.view.print_sucess(f"Le tournoi {new_tourney.get_field('name')['value']} a été créé")
        else:
            self.base_ctrl.delete_tourney_by_index(new_tourney_index)
            return False

        return new_tourney_index


if __name__ == '__main__':
    pass