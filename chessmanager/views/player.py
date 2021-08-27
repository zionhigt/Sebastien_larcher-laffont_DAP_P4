from chessmanager.views.view import View

from termcolor import colored as _c

from datetime import date

class PlayerView(View):
    def __init__(self):
        super().__init__()
        self.path = "Chessmanager>Joueurs>"

    def compute_age(self, birthday):

        birth_date = date.fromisoformat(birthday)
        birth_year = birth_date.year
        now_date = date.today()
        return (now_date.year - birth_year)

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
            print(_c(f"\nListe des joueurs", "grey", "on_yellow"))
            self.print_table(head, players_info)
   