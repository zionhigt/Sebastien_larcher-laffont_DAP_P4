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
                x.first_name['value'],
                x.last_name['value'],
                self.compute_age(x.at_date['value']),
                str(x.score),
                str(x.rating)
            ], available_players))
        head = ['Prénom', 'Nom', 'Age', 'Score', 'Classement']
        if len(players_info) > 0:
            print(_c(f"\nListe des joueurs", "grey", "on_yellow"))
            self.print_table(head, players_info)
   