from chester.models.tourney import Tourney

from termcolor import colored as _c


def start():
    print("Le tournoi a demaré")


class TourneyCtrl:
    def __init__(self, view, base_ctrl):
        self.view = view
        self.base_ctrl = base_ctrl
        self.tourney_model = None
        self.start = False
        self.current_tourney_index = None
        # {text, hidden, callback}
        self.loaded_actions = [
            ('Liste des joueurs', True, 'show_players'),
            ('Ajouter des joueurs', False, 'add_player'),
            ('Démarer le tournoi', True, 'start'),
            ('Retour à la sélection', False, 'return')
        ]

        self.loaded_action_callback = {
            'show_players': self.show_players,
            'add_player': self.add_player,
            'start': self.start,
            'return': self.run
        }

        self.unloaded_actions = [
            ('Créer un tournois', False, 'create_tourney'),
            ('Charger un tournoi', True, 'load_tourney'),
            ('Liste des tournois', True, 'show_tourneys'),
            ('Retour au menu principal', False, 'return')
        ]

        self.unloaded_action_callback = {
            'create_tourney': self.create_tourney,
            'load_tourney': self.asking_for_load_tourneys,
            'show_tourneys': self.show_tourneys,
            'return': self.exit
        }
    def exit(self):
        return False

    def loaded_actions_rules(self):
        base_actions = list(map(lambda x: list(x), self.loaded_actions))
        if len(self.tourney_model.players) != 0:
            base_actions[0][1] = False
        if not len(self.tourney_model.players) < 2:
            base_actions[2][1] = False
        
        return base_actions
    
    def unloaded_actions_rules(self):
        base_actions = list(map(lambda x: list(x), self.unloaded_actions))
        if len(self.base_ctrl.get_all_tourney()) != 0:
            base_actions[1][1] = False
            base_actions[2][1] = False
        
        return base_actions

    def compute_available_action(self, rules):
        base_actions = rules()
        actions = filter(lambda x: not x[1], base_actions)
        return actions

    def add_player(self):
        added_player = self.base_ctrl.add_player()
        player = self.base_ctrl.get_player_by_index(added_player)
        print(added_player)
        self.tourney_model.add_player(added_player)
        self.view.asking_for_model(player)
        player.load()
        self.show_loaded_actions()
        return

    def show_players(self):
        print(_c(f"\nListe des joueurs du tournoi {self.tourney_model.name['value']}", "grey", "on_yellow"))
        players = list(map(lambda x: self.base_ctrl.get_player_by_index(x), self.tourney_model.players))
        
        self.view.show_available_players(players)
        self.show_loaded_actions()
        return

    def show_loaded_actions(self):
        actions_available = list(self.compute_available_action(self.loaded_actions_rules))
        user_choice = self.view.show(actions_available)
        callback_name = actions_available[int(user_choice)][2]
        callback_methode = self.loaded_action_callback[callback_name]
        callback_methode()
        return
    
    def show_unloaded_actions(self):
        actions_available = list(self.compute_available_action(self.unloaded_actions_rules))
        user_choice = self.view.show(actions_available)
        callback_name = actions_available[int(user_choice)][2]
        callback_methode = self.unloaded_action_callback[callback_name]
        callback_methode()
        return 0

    def asking_for_load_tourneys(self):
        tourney_index = self.view.ask_for_load_tourney(self.base_ctrl.get_all_tourney())
        self.load_tourney(int(tourney_index))
        return

    def show_tourneys(self):
        self.view.show_tourneys_table(self.base_ctrl.get_all_tourney())
        self.show_unloaded_actions()
        return


    def load_tourney(self, tourney_index):
        
        tourney = self.base_ctrl.get_tourney_by_index(tourney_index)
        if tourney.load():
            self.tourney_model = tourney
            self.show_loaded_actions()
        else:
            print('Ce tournoi ne peux pas être chargé')
        return

    def create_tourney(self):
        new_tourney = self.tourney_maker()
        is_tourney_to_load = self.view.ask(f"Charger ce tournoi {_c('[O/N]', 'grey', 'on_white')} ?")
        is_tourney_to_load = is_tourney_to_load.upper()
        if is_tourney_to_load == "O":
            self.current_tourney_index = new_tourney
            self.load_tourney(new_tourney)

        elif is_tourney_to_load == 'N':
            self.show_unloaded_actions()
        return
    def run(self):
        # tourney_index = self.view.ask_for_load_tourney(self.base_ctrl.get_all_tourney())
        self.show_unloaded_actions()
        # if tourney_index != "c":
        #     self.current_tourney_index = int(tourney_index)
        # else:
        #     if not self.create_tourney():
        #         self.run()
            

        # if self.current_tourney_index is not None:
        #     self.load_tourney(self.current_tourney_index)

    def tourney_maker(self):

        # return index of global list
        added_tourney = self.base_ctrl.add_tourney()
        tourney = self.base_ctrl.get_tourney_by_index(added_tourney)
        self.view.asking_for_model(tourney)

        return added_tourney


if __name__ == '__main__':

    print(Tourney)
