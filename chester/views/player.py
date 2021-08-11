from chester.views.view import View

from termcolor import colored as _c

class PlayerView(View):
    def show_available_players(self, available_players):
        players_info = list(map(lambda x: [x.first_name['value'], x.last_name['value'], x.at_date['value']], available_players))
        head = ['Prénom', 'Nom', 'Date']
        if len(players_info) > 0:
            print(_c(f"\nListe des joueurs", "grey", "on_yellow"))
            self.print_table(head, players_info)  