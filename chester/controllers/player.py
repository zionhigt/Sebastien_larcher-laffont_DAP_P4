class PlayerCtrl:
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
            'add_player': self.run,
            'return': self.exit
        }

    def actions_rules(self):
        base_actions = list(map(lambda x: list(x), self.base_actions))
        if len(self.base_ctrl.get_all_players()) != 0:
            base_actions[0][1] = False
        
        return base_actions

    def compute_available_action(self, rules):
        base_actions = rules()
        actions = filter(lambda x: not x[1], base_actions)
        return actions

    def show_players(self):
        players = self.base_ctrl.get_all_players()
        self.view.show_available_players(players)
        self.show_actions()
        return

    def exit(self):
        return False

    def show_actions(self):
        actions_available = list(self.compute_available_action(self.actions_rules))
        user_choice = self.view.show(actions_available)
        callback_name = actions_available[int(user_choice)][2]
        callback_methode = self.actions_callbacks[callback_name]
        callback_methode()
        return

    def run(self):
        self.show_actions()
        return

