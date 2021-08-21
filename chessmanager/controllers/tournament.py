from chessmanager.models.tournament import Tournament
from chessmanager.models.round import Round
from chessmanager.controllers.ctrl import Ctrl
from chessmanager.controllers.round import RoundCtrl
from chessmanager.controllers.ctrl import compute_available_action

from termcolor import colored as _c
from chessmanager.views.round import RoundView

ROUND_VIEW = RoundView()

class TournamentCtrl(Ctrl):
    def __init__(self, view, base_ctrl):
        self.view = view
        self.roundCtrl = RoundCtrl(ROUND_VIEW) 
        self.base_ctrl = base_ctrl
        self.tournament_model = None
        self.current_tournament_index = None
        self.current_round = None
        # {text, hidden, callback}
        self.base_actions = [
            ('Liste des joueurs par noms', True, 'show_players_by_name'),
            ('Classement du tournois', True, 'show_players_by_score'),
            ('Ajouter des joueurs', False, 'add_player'),
            ('Démarer le tournoi', True, 'start'),
            ('Liste des rondes', True, 'show_rounds'),
            ('Éditer la ronde en cours', True, 'run_round'),
            ('Terminer le tournoi', True, 'mark_as_done'),
            ('Voir les matchs d\'une ronde', True, 'show_round_matchs'),
            ('Voir les matchs du tournois', True, 'show_tournament_matchs'),
            ('Retour à la sélection', False, 'return')
        ]

        self.action_callback = {
            'show_players_by_name': self.show_players('name'),
            'show_players_by_score': self.show_players('score'),
            'add_player': self.add_player,
            'start': self.start,
            'show_rounds': self.show_rounds,
            'run_round': self.run_round,
            'mark_as_done': self.mark_as_done,
            'show_round_matchs': self.show_round_matchs,
            'show_tournament_matchs': self.show_tournament_matchs,
            'return': self.exit
        }
    def show_round_matchs(self):
        self.view.show_available_rounds(self.tournament_model.rounds, select=True)
        round_choiced = self.view.ask("\nEntrez l'ID de la ronde")

        if int(round_choiced) in range(len(self.tournament_model.rounds)):
            t_round = self.tournament_model.rounds[int(round_choiced)]
            self.view.show_available_matchs(t_round.matchs)
        self.show_available_actions()

    def show_tournament_matchs(self):
        tournament_matchs = [matchs for t_round in self.tournament_model.rounds for matchs in t_round.matchs]
        self.view.show_available_matchs(tournament_matchs)
        self.show_available_actions()

    def mark_as_done(self):
        self.tournament_model.ended = True
        self.tournament_model.state = "DONE"
        return

    def run_round(self):
        self.roundCtrl.run(self.tournament_model.rounds)
        if self.current_round.state == "DONE":
            self.tournament_model.update_players_scores()
            self.add_round()
        self.show_available_actions()

    def start(self):
        self.add_round()
        self.tournament_model.started = True
        self.tournament_model.state = "PROCESS"
        self.show_available_actions()

    def show_rounds(self):
        self.view.show_available_rounds(self.tournament_model.rounds)
        self.show_available_actions()

    def add_round(self):
        if len(self.tournament_model.rounds) < self.tournament_model.turns['value']:
            round_name = f"Round_{len(self.tournament_model.rounds) + 1}"
            self.current_round = Round(round_name)
            self.tournament_model.add_round(self.current_round)
            self.current_round.players = self.get_players_sorted_by_rate(self.tournament_model.players, reverse=False)
            if len(self.tournament_model.rounds) > 1:
                players_by_rate = self.get_players_sorted_by_rate(self.tournament_model.players, reverse=False)
                self.current_round.players = self.get_players_sorted_by_score(players_by_rate)

            self.roundCtrl.run(self.tournament_model.rounds, persistant=False)


        return

    @compute_available_action
    def actions_rules(self):
        """Define what field will be show when tournament will be loaded"""

        base_actions = list(map(lambda x: list(x), self.base_actions))
        if len(self.tournament_model.players) != 0:
            base_actions[0][1] = False
            base_actions[1][1] = False

        base_actions[2][1] = self.tournament_model.started
        
        if len(self.tournament_model.players) >= 2 and not self.tournament_model.started:
            base_actions[3][1] = False

        base_actions[4][1] = not self.tournament_model.started

        if self.current_round and self.current_round.state != "DONE":
            base_actions[5][1] = False

        if len(self.tournament_model.rounds) == self.tournament_model.turns['value'] and not self.tournament_model.ended:
            if self.tournament_model.rounds[-1].state == "DONE":
                base_actions[6][1] = False

        if len(self.tournament_model.rounds) != 0:
            base_actions[7][1] = False
            base_actions[8][1] = False

        return base_actions

    def add_player(self):
        """Asking user to load an already known player or create a new one.
        Adding this player in the loaded tournament.
        """
        is_quit = False
        players_not_in = self.get_players_not_in_tournament()
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
            self.tournament_model.add_players(players)
            if len(players) > 0:
                sucess_message = f"à été ajouté au tounois {self.tournament_model.name['value']}"
                if len(players) > 1:
                    sucess_message = f"\nont été ajoutés au tounois {self.tournament_model.name['value']}"

                players_texts = list(map(lambda x: f"{x.first_name['value']} {x.last_name['value']}", players)) 
                sucess_text = "\n".join(players_texts) + sucess_message
                self.view.print_sucess(sucess_text)

        self.show_available_actions()
        return


    def get_players_not_in_tournament(self):
        """Give already known players not in this loaded tournament
        """

        players = self.base_ctrl.get_all_players()
        players_not_in = list(filter(lambda x: x not in self.tournament_model.players, players))

        return players_not_in

    def get_tournament_player_score(self, player):
        all_players = [p[0] for p in self.touney_model.players]
        player_index = all_players.index(player)
        return self.tournament_model.player[player_index][1]

    def get_players_sorted_by_name(self, available_players):
        sorted_players = sorted(available_players, key=lambda x: x[0].last_name['value'])
        return sorted_players

    def get_players_sorted_by_rate(self, available_players, reverse=True):

        sorted_players = sorted(available_players, key=lambda x: x[0].rating['value'], reverse=reverse)
        return sorted_players

    def get_players_sorted_by_score(self, available_players):
        sorted_players = sorted(available_players, key=lambda x: x[1], reverse=True)
        return sorted_players

    def show_players(self, sort=None):
        """Showing this loaded tournament players
        """
        def closure():
            print(_c(f"\nListe des joueurs du tournoi {self.tournament_model.name['value']}", "grey", "on_yellow"))
            sorts_methods = {
                'name': self.get_players_sorted_by_name,
                'score': self.get_players_sorted_by_score
            }

            all_players = self.tournament_model.players

            if sort is None or sort not in sorts_methods.keys():
                players = (all_players)
            else:
                players = sorts_methods[sort](all_players)
    
            self.view.show_available_players(players)
            self.show_available_actions()
            return
        return closure

    def show_available_actions(self):
        """Showing availables actions for this loaded tournament
        """
        actions_available = self.actions_rules()
        self.show_actions(actions_available, self.action_callback)
        return

    def run(self, tournament):
        self.tournament_model = tournament
        self.view.compute_path(tournament.name['value'])
        self.show_available_actions()

        return

if __name__ == '__main__':
    pass