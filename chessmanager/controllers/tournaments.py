from chessmanager.controllers.ctrl import Ctrl
from chessmanager.controllers.ctrl import compute_available_action

from chessmanager.views.tournament import TournamentView
from chessmanager.controllers.tournament import TournamentCtrl
from chessmanager.models.tournament import Tournament

from termcolor import colored as _c

class TournamentsCtrl(Ctrl):
    def __init__(self, view, base_ctrl):
        self.view = view
        self.base_ctrl = base_ctrl
        self.tournament_ctrl = TournamentCtrl(TournamentView(), self.base_ctrl)

        # {text, hidden, callback}
        self.base_actions = [
            ('Créer un tournois', False, 'create_tournament'),
            ('Charger un tournoi', True, 'load_tournament'),
            ('Liste des tournois', True, 'show_tournaments'),
            ('Retour au menu principal', False, 'return'),
            ('Aide', False, 'show_helper')
        ]

        self.action_callback = {
            'create_tournament': self.create_tournament,
            'load_tournament': self.asking_for_load_tournaments,
            'show_tournaments': self.show_tournaments,
            'return': self.exit,
            'show_helper': self.show_helper
        }

    def show_helper(self):
        self.view.show_helper()
        self.show_available_actions()
        return
    
    @compute_available_action
    def actions_rules(self):
        """Define what field will be show when tournament will be unloaded"""

        base_actions = list(map(lambda x: list(x), self.base_actions))
        if len(self.base_ctrl.get_all_tournament()) != 0:
            base_actions[1][1] = False
            base_actions[2][1] = False
        
        return base_actions

    def show_available_actions(self):
        """Showing availables actions when no tournament has loaded
        """

        actions_available = self.actions_rules()
        self.show_actions(actions_available, self.action_callback)
        return 

    def asking_for_load_tournaments(self):
        """Asking user to load an available tournament
        """
        tournament_index = self.view.ask_for_load_tournament(self.base_ctrl.get_all_tournament())
        self.load_tournament(int(tournament_index))
        return

    def show_tournaments(self):
        """Showing availables tournament
        """

        self.view.show_tournaments_table(self.base_ctrl.get_all_tournament())
        self.show_available_actions()
        return


    def load_tournament(self, tournament_index):
        """Turn a tournament to load
        Arguments:
            tournament_index -- index of the tournament saved into the base controller 
        """

        tournament = self.base_ctrl.get_tournament_by_index(tournament_index)
        if tournament.load():
            # self.show_loaded_actions()
            self.tournament_ctrl.run(tournament)
            self.show_available_actions()
        else:
            print('Ce tournoi ne peux pas être chargé')
        return

    def create_tournament(self):
        """Asking user for tournament informations
        """
        new_tournament = self.tournament_maker()
        if new_tournament != False:
            is_tournament_to_load = self.view.ask(f"Charger ce tournoi {_c('[O/N]', 'grey', 'on_white')} ?")
            if is_tournament_to_load.upper() == "O":
                self.current_tournament_index = new_tournament
                self.load_tournament(new_tournament)

            elif is_tournament_to_load.upper() == 'N':
                self.show_available_actions()

        self.show_available_actions()
        return

    def run(self):
        self.show_available_actions()
        return

    def tournament_maker(self):
        # return index of global list
        new_tournament_index = self.base_ctrl.add_tournament()
        new_tournament = self.base_ctrl.get_tournament_by_index(new_tournament_index)
        if self.view.asking_for_model(new_tournament) != False:
            self.view.print_sucess(f"Le tournoi {new_tournament.get_field('name')['value']} a été créé")
        else:
            self.base_ctrl.delete_tournament_by_index(new_tournament_index)
            return False

        return new_tournament_index


if __name__ == '__main__':
    pass