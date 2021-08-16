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
            ('Liste des joueurs par noms', True, 'show_players_by_name'),
            ('Liste des joueurs par scores', True, 'show_players_by_score'),
            ('Ajouter des joueurs', False, 'add_player'),
            ('Démarer le tournoi', True, 'start'),
            ('Retour à la sélection', False, 'return')
        ]

        self.action_callback = {
            'show_players_by_name': self.show_players('name'),
            'show_players_by_score': self.show_players('score'),
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
            base_actions[1][1] = False

        if not len(self.tourney_model.players) < 2:
            base_actions[2][1] = False
        
        return base_actions

    def add_player(self):
        """Asking user to load an already known player or create a new.
        Adding this player in the loaded tourney.
        """
        is_quit = False
        players_not_in = self.get_players_not_in_tourney()
        self.view.show_available_players(players_not_in, select=True)
        user_choice = self.view.ask("\nEntrez les ID séparés par un espace \nEntrez 'c' pour créer un joueur ")
        players = self.base_ctrl.get_all_players()
        if user_choice == 'c':
            new_player_index = self.base_ctrl.add_player()
            player = self.base_ctrl.get_player_by_index(new_player_index)
            if self.view.asking_for_model(player) != False:
                player.load()
                players = [player]
            else:
                self.base_ctrl.delete_player_by_index(new_player_index)
                is_quit = True
        else:
            user_choices = user_choice.split(' ')
            players = []
            for choiced_player in user_choices:
                if choiced_player != '':
                    if int(choiced_player) in range(0, len(players_not_in)):
                        players.append(players_not_in[int(choiced_player)])
                
        if not is_quit:
            self.tourney_model.add_players(players)
            if len(players) > 0:
                sucess_message = f"à été ajouté au tounois {self.tourney_model.name['value']}"
                if len(players) > 1:
                    sucess_message = f"\nont été ajoutés au tounois {self.tourney_model.name['value']}"

                players_texts = list(map(lambda x: f"{x.first_name['value']} {x.last_name['value']}", players)) 
                sucess_text = "\n".join(players_texts) + sucess_message
                self.view.print_sucess(sucess_text)

        self.show_available_actions()
        return

    def get_players_not_in_tourney(self):
        """Give already known players not in this loaded tourney
        """

        players = self.base_ctrl.get_all_players()
        players_not_in = list(filter(lambda x: x not in self.tourney_model.players, players))

        return players_not_in

    def get_players_sorted_by_name(self, available_players):
        sorted_player = sorted(available_players, key=lambda x: x.first_name['value'])
        return sorted_player

    def get_players_sorted_by_score(self, available_players):
        sorted_player = sorted(available_players, key=lambda x: x.score, reverse=True)
        return sorted_player

    def show_players(self, sort=None):
        """Showing this loaded tourney players
        """
        def closure():
            print(_c(f"\nListe des joueurs du tournoi {self.tourney_model.name['value']}", "grey", "on_yellow"))
            sorts_methods = {
                'name': self.get_players_sorted_by_name,
                'score': self.get_players_sorted_by_score
            }

            all_players = self.tourney_model.players

            if sort is None:
                players = all_players
            else:
                players = sorts_methods[sort](all_players)
            
            self.view.show_available_players(players)
            self.show_available_actions()
            return
        return closure

    def show_available_actions(self):
        """Showing availables actions for this loaded tourney
        """

        actions_available = self.actions_rules()
        self.show_actions(actions_available, self.action_callback)
        return

    def run(self, tourney):
        self.tourney_model = tourney
        self.view.compute_path(tourney.name['value'])
        self.show_available_actions()

        return

if __name__ == '__main__':
    pass