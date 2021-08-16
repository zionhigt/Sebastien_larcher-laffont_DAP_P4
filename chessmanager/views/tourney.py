from chessmanager.views.view import View

from termcolor import colored as _c

from datetime import date

class TourneyView(View):
    def __init__(self):
        self.path = self.compute_path()

    def compute_path(self, current_name="Tounoi"):
        self.path = "Chessmanager>Tournois>" + current_name + ">"

    def compute_age(self, birthday):

        birth_date = date.fromisoformat(birthday)
        birth_year = birth_date.year
        now_date = date.today()
        return (now_date.year - birth_year)

    def show_available_players(self, available_players, select=False):
        players_index = range(len(available_players))
        head = ['ID', 'Prénom', 'Nom', 'Age', 'Score', 'Classement']
        players_info = list(map(lambda x, y: [
                str(y),
                x.first_name['value'],
                x.last_name['value'],
                self.compute_age(x.at_date['value']),
                str(x.score),
                str(x.rating)
            ], available_players, players_index))

        if len(players_info) > 0:
            if not select:
                head = head[1:]
                players_info = list(map(lambda x: x[1:], players_info))
            self.print_table(head, players_info)

if __name__ == '__main__':

    print()
    print(TourneyView.show.__doc__)

