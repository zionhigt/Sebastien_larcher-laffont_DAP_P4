from chessmanager.views.view import View

from termcolor import colored as _c


class PlayerView(View):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def show_available_players(self, available_players):
        print(self.path)
        players_info = list(map(lambda x: [
                str(x.rating),
                x.last_name['value'],
                x.first_name['value'],
                self.compute_age(x.birth_date['value'])
            ], available_players))
        head = ['Place', 'Nom', 'Prénom', 'Age']
        if len(players_info) > 0:
            print(_c("\nListe des joueurs", "grey", "on_yellow"))
            self.print_table(head, players_info)
