from chessmanager.views.view import View

from termcolor import colored as _c

from datetime import date

class TourneysView(View):
    def __init__(self):
        self.exemple_required_with_default = self.format_question_from_field("champ requis",{'required': True,'default': "Valeur par default"})
        self.exemple_required_without_default = self.format_question_from_field("champ requis",{'required': True,'default': ""})
        self.exemple_norequired_without_default = self.format_question_from_field("champ requis",{'required': False,'default': ""})
        self.helper_field = f"""{self.exemple_required_with_default}    Champ requis, Appuyez sur entrer pour selectioner la valeur par default 
        {self.exemple_required_without_default}     Champ requis, Entrez une valeur correcte pour ce champ
        {self.exemple_norequired_without_default}   Champ non requis, ENTRER pour laisser vide

        [/q]    Annuler l'édition
        [help]  Afficher cette aide
        """
        self.helper_menu = "Pour naviguer dans les menus, entrez le numeros de ligne de l'actions"
    
    def show_unloaded_helper(self):
        self.print_help(self.helper_unloaded_menu)
        return

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

