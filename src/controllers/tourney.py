from src.models.tourney import Tourney

class TourneyCtrl:
    def __init__(self, view, base_ctrl):
        self.view = view
        self.base_ctrl = base_ctrl
        self.tourney_model = None
        self.start = False
        # {text, hidden, callback}
        self.base_actions = [
            ('Liste des joueurs', True, 'show_players'),
            ('Ajouter des joueurs', False, 'add_player'),
            ('Démarer le tournoi', True, 'start'),
        ]

        self.actions_callbacks = {
            'show_players': self.show_players,
            'add_player': self.add_player,
            'start': self.start
        }


    def create_tourney(self):
        self.view.asking_create_tourney(self.tourney_model.get_schema())

    def compute_available_action(self):
        base_actions = list(map(lambda x: list(x), self.base_actions))
        if len(self.tourney_model.players) != 0:
            base_actions[0][1] = False
        if not len(self.tourney_model.players) < 2:
            base_actions[2][1] = False
            
        actions = filter(lambda x: not x[1], base_actions)
        self.base_actions = list(map(lambda x: tuple(x), base_actions))
        return actions

    def add_player(self):
        added_player = self.base_ctrl.add_player()
        self.tourney_model.players.append(added_player)
        player = self.base_ctrl.get_player_by_index(added_player)
        self.view.asking_for_model(player)
        player.load()
        self.show_actions()
        
    
    def show_players(self):
        print("See player")
        players = list(map(lambda x: self.base_ctrl.get_player_by_index(x), self.tourney_model.players))
        players_info = list(map(lambda x: f"{x.first_name} {x.last_name}", players))
        print("\n".join(players_info))
        self.show_actions()
    
    def start(self):
        print("Le tournoi a demaré")
    
    def show_actions(self):
        actions_available = list(self.compute_available_action())
        user_choice = self.view.show(actions_available)
        callback_name = actions_available[int(user_choice)][2]
        callback_methode = self.actions_callbacks[callback_name]
        callback_methode()

    def load_tourney(self, tourney_index):
        
        tourney = self.base_ctrl.get_tourney_by_index(tourney_index)
        if tourney.load():
            self.tourney_model = tourney
            self.show_actions()
        else:
            print('Ce tournoi ne peux pas être chargé')


if __name__ == '__main__':

    print(Tourney)
