from chessmanager.views.view import View
from chessmanager.local.local import t as _t

from termcolor import colored as _c


class TournamentsView(View):
    def __init__(self, path):
        super().__init__()

        self.path = path

    def show_tournaments_table(self, available_tournaments, select=False):

        tournaments_indexs = list(range(len(available_tournaments)))
        head_table = ["ID", "Nom", "Lieu", "Date", "Description", "État"]
        body_table = list(map(lambda x, y: [
            str(y),
            x.name['value'],
            x.at_place['value'],
            x.at_date['value'],
            x.comment['value'],
            _t(x.state)
            ], available_tournaments, tournaments_indexs))

        if len(body_table) > 0:
            if not select:
                head_table = head_table[1:]
                body_table = list(map(lambda x: x[1:], body_table))
            self.print_table(head_table, body_table)
        else:
            print("")

    def ask_for_load_tournament(self, available_tournament):
        self.show_tournaments_table(available_tournament, select=True)
        response_input = self.ask(f"\nPour charger un tournois entrez son {_c('ID', 'grey', 'on_white')}")
        return response_input
