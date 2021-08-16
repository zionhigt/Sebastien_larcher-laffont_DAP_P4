from chessmanager.views.view import View

from termcolor import colored as _c

from datetime import date

class TourneysView(View):
    def __init__(self):
        super().__init__()

        self.path = "Chessmanager>Tournois>"
    
    def show_unloaded_helper(self):
        self.print_help(self.helper_unloaded_menu)
        return

    def show_tourneys_table(self, available_tourneys, select=False):

        tourneys_indexs = list(range(len(available_tourneys)))
        head_table = ["ID", "Nom", "Lieu", "Date", "Description"]
        body_table = list(map(lambda x, y: [
            str(y),
            x.name['value'],
            x.at_place['value'],
            x.at_date['value'],
            x.comment['value']
            ], available_tourneys, tourneys_indexs))

        if len(body_table) > 0:
            print(select)
            if not select:
                head_table = head_table[1:]
                body_table = list(map(lambda x: x[1:], body_table))
            self.print_table(head_table, body_table)
        else:
            print("")

    def ask_for_load_tourney(self, available_tourney):
        self.show_tourneys_table(available_tourney, select=True)
        response_input = self.ask(f"\nPour charger un tournois entrez son {_c('ID', 'grey', 'on_white')}")
        return response_input
        
if __name__ == '__main__':

    print()
    print(TourneyView.show.__doc__)

