from chessmanager.controllers.ctrl import Ctrl
from chessmanager.controllers.ctrl import compute_available_action

class PlayerCtrl(Ctrl):
    def __init__(self, view, base_ctrl):
        self.base_ctrl = base_ctrl
        self.view = view

        self.base_actions = [
            ('Liste des joueurs', True, 'show_players'),
            ('Ajouter un joueurs', False, 'add_player'),
            ('Retour au menu principal', False, 'return')
        ]

        self.actions_callbacks = {
            'show_players': self.show_players,
            'add_player': self.add_player,
            'return': self.exit
        }

    @compute_available_action
    def actions_rules(self):
        base_actions = list(map(lambda x: list(x), self.base_actions))
        if len(self.base_ctrl.get_all_players()) != 0:
            base_actions[0][1] = False
        
        return base_actions

    def show_players(self):
        players = self.base_ctrl.get_all_players()
        self.view.show_available_players(players)
        self.show_available_actions()
        return

    def show_available_actions(self):
        actions_available = self.actions_rules()
        self.show_actions(actions_available, self.actions_callbacks)
        return

    def add_player(self):
        new_player_index = self.base_ctrl.add_player()
        new_player = self.base_ctrl.get_player_by_index(new_player_index)
        
        if self.view.asking_for_model(new_player) != False:
            new_player.load()
            self.view.print_sucess(f"{new_player.first_name['value']} {new_player.last_name['value']} à été ajouté")
        else:
            self.base_ctrl.delete_player_by_index(new_player_index)

        self.run()
        return

    def run(self):
        self.show_available_actions()
        return

