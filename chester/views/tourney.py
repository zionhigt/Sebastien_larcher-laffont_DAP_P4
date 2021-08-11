from chester.views.view import View

from termcolor import colored as _c

from datetime import date

class TourneyView(View):

    def show_available_players(self, available_players):
        players_info = list(map(lambda x: [x.first_name['value'], x.last_name['value'], x.at_date['value']], available_players))
        head = ['Prénom', 'Nom', 'Date']
        if len(players_info) > 0:
            self.print_table(head, players_info)    

    def show_tourneys_table(self, available_tourney):
        i = 0
        head_table = ["ID", "Nom", "Lieu", "Date", "Description"]
        body_table = []
        for tourney in available_tourney:
            tourney = tourney.get_schema_input()
            body_table.append([str(i), tourney['name']['value'], tourney['at_place']['value'], tourney['at_date']['value'], tourney['comment']['value']])
            i+=1
        if i > 0:
            self.print_table(head_table, body_table)
        else:
            print("")

    def ask_for_load_tourney(self, available_tourney):
        self.show_tourneys_table(available_tourney)
        response_input = self.ask(f"Pour charger un tournois entrez son {_c('ID', 'grey', 'on_white')}")
        return response_input
        
if __name__ == '__main__':

    print()
    print(TourneyView.show.__doc__)

