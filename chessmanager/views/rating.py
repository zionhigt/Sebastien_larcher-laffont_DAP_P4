from chessmanager.views.view import View

from termcolor import colored as _c


class RatingView(View):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def show_available_players(self, available_players):
        players_index = range(len(available_players))
        players_info = list(map(lambda x, y: [
                str(y),
                str(x.rating),
                x.last_name['value'],
                x.first_name['value'],
                self.compute_age(x.birth_date['value'])
            ], available_players, players_index))
        head = ['ID', 'Place', 'Nom', 'Prénom', 'Age']
        if len(players_info) > 0:
            print(_c("\nListe des joueurs", "grey", "on_yellow"))
            self.print_table(head, players_info)
