from chessmanager.views.view import View

from termcolor import colored as _c

from datetime import date

class TourneyView(View):
    
    def show_available_players(self, available_players):
        players_ids = range(len(available_players))
        players_info = list(map(lambda x, i: [str(i), x.first_name['value'], x.last_name['value'], x.at_date['value']], available_players, players_ids))
        head = ['ID', 'Prénom', 'Nom', 'Date']
        if len(players_info) > 0:
            self.print_table(head, players_info)
        print('\n')
        
if __name__ == '__main__':

    print()
    print(TourneyView.show.__doc__)

