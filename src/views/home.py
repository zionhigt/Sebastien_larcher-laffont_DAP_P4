from .view import View

class HomeView(View):

    def ask_for_load_tourney(self, available_tourney):
        i = 0
        for tourney in available_tourney:
            tourney = tourney.get_schema_input()
            print(f"{i}. {tourney['name']['value']}\t{tourney['at_date']['value']}\t{tourney['at_place']['value']}")
            i+=1
        response_input = self.ask("Chargez un tournoi ou entrez 'c' pour en créer un")
        return response_input

   
if __name__ == '__main__':

    print()
    print(HomeView.show.__doc__)