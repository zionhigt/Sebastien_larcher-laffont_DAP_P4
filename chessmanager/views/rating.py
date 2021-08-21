from chessmanager.views.view import View

from termcolor import colored as _c
from datetime import date

class RatingView(View):
    def compute_age(self, birthday):

        birth_date = date.fromisoformat(birthday)
        birth_year = birth_date.year
        now_date = date.today()
        return (now_date.year - birth_year)

    def show_available_players(self, available_players):
        players_index = range(len(available_players))
        players_info = list(map(lambda x, y: [
                str(y),
                str(x.rating['value']),
                x.last_name['value'],
                x.first_name['value'],
                self.compute_age(x.at_date['value'])
            ], available_players, players_index))
        head = ['ID', 'Place', 'Nom', 'Prénom', 'Age']
        if len(players_info) > 0:
            print(_c(f"\nListe des joueurs", "grey", "on_yellow"))
            self.print_table(head, players_info)