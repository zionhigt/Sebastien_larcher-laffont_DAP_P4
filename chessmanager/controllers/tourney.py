from chessmanager.models.tourney import Tourney
from chessmanager.controllers.ctrl import Ctrl
from chessmanager.controllers.ctrl import compute_available_action

from termcolor import colored as _c

class TourneyCtrl(Ctrl):
    def __init__(self, view, base_ctrl):
        self.view = view
        self.base_ctrl = base_ctrl
        self.tourney_model = None
        self.start = False
        self.current_tourney_index = None
        # {text, hidden, callback}
        self.base_actions = [
            ('Liste des joueurs', True, 'show_players'),
            ('Ajouter des joueurs', False, 'add_player'),
            ('Démarer le tournoi', True, 'start'),
            ('Retour à la sélection', False, 'return')
        ]

        self.action_callback = {
            'show_players': self.show_players,
            'add_player': self.add_player,
            'start': self.start,
            'return': self.exit
        }
        
    @compute_available_action
    def actions_rules(self):
        """Define what field will be show when tourney will be loaded"""

        base_actions = list(map(lambda x: list(x), self.base_actions))
        if len(self.tourney_model.players) != 0:
            base_actions[0][1] = False
        if not len(self.tourney_model.players) < 2:
            base_actions[2][1] = False
        
        return base_actions

    def add_player(self):
        """Asking user to load an already known player or create a new.
        Adding this player in the loaded tourney.
        """
        is_quit = False
        players_not_in = self.get_players_not_in_tourney()
        self.view.show_available_players(players_not_in)
        user_choice = self.view.ask("Entrez un ID ou entrez 'c' pour créer un joueur ")
        players = self.base_ctrl.get_all_players()
        if user_choice == 'c':
            new_player_index = self.base_ctrl.add_player()
            player = self.base_ctrl.get_player_by_index(new_player_index)
            if self.view.asking_for_model(player) != False:
                player.load()
            else:
                self.base_ctrl.delete_player_by_index(new_player_index)
                is_quit = True
        else:
            player = players_not_in[int(user_choice)]

        if not is_quit:
            self.tourney_model.add_player(player)
            sucess_text = f"{player.first_name['value']} {player.last_name['value']} à été ajouté au tournoi {self.tourney_model.name['value']}"
            self.view.print_sucess(sucess_text)

        self.show_available_actions()
        return

    def get_players_not_in_tourney(self):
        """Give already known players not in this loaded tourney
        """

        players = self.base_ctrl.get_all_players()
        players_not_in = list(filter(lambda x: x not in self.tourney_model.players, players))

        return players_not_in

    def show_players(self):
        """Showing this loaded tourney players
        """

        print(_c(f"\nListe des joueurs du tournoi {self.tourney_model.name['value']}", "grey", "on_yellow"))
        players = self.tourney_model.players
        
        self.view.show_available_players(players)
        self.show_available_actions()
        return

    def show_available_actions(self):
        """Showing availables actions for this loaded tourney
        """

        actions_available = self.actions_rules()
        self.show_actions(actions_available, self.action_callback)
        return

    def run(self, tourney):
        self.tourney_model = tourney
        self.show_available_actions()

        return

if __name__ == '__main__':
    pass