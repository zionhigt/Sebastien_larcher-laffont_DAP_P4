from chessmanager.views.table import Table
from chessmanager.local.local import Local

import sys
from datetime import date
from termcolor import colored as _c

LOCAL = Local()
_t = LOCAL._t

class View:
    def __init__(self):
        self.path = "Chessmanager>"
        self.exemple_default = _c('Valeur par défaut', 'yellow')
        self.exemple_required_without_default = self.format_question_from_field("Champ requis",{'required': True,'default': ""})
        self.exemple_norequired_without_default = self.format_question_from_field("Optionel",{'required': False,'default': ""})
        self.helper_field_list = [
            _c("----------------------------------------------------------------------------------\n", 'white'),
            f"({self.exemple_default})\t|ENTRER| pour conserver la valeur par default\n",
            f"{self.exemple_required_without_default}\tEntrez une valeur correcte pour ce champ\n",
            f"{self.exemple_norequired_without_default}\t\t|ENTRER| pour laisser vide\n",
            "[/q]\t\t\tQuitter l'édition\n",
            "[help]\t\t\tAfficher cette aide\n",
            "----------------------------------------------------------------------------------\n"
        ]

        self.helper_field = "\n".join(self.helper_field_list)
        self.helper_menu = "Pour naviguer dans les menus, entrez le numeros de ligne de l'actions"
    def get_helper_menu(self):
        return self.helper_menu

    def get_helper_field(self):
        return self.helper_field

    def ask(self, question, lazy=True):
        response_input = input(f"\r{question} {_c(':', 'yellow')} ")
        if not lazy:
            if response_input == '':
                return self.ask(question, False)
            
        return response_input

    def format_question_from_field(self, field_name, field_config):

        field_name = f" {_t(field_name)} "
        if field_config['required']:
            field_text = f"{_c(field_name, 'grey', 'on_white')}{_c('*', 'red', 'on_white')}"
        else: 
            field_text = f"{_c(field_name, 'grey', 'on_white')}"

        if field_config['default'] != "" and field_config['default'] is not None:
            default_value = field_config['default']
            if field_config['type'] is date:
                default_value = self.format_date(field_config['default'])
            default = f"({_c(default_value, 'yellow')})"
        else:
            default =  ""

        return f"{field_text}> {default}"

    def format_date(self, date_str):
        date_cls = date.fromisoformat(date_str)
        return date_cls.strftime("%d/%m/%Y")

    def asking_for_date(self, date_field):
        default_date = date_field['default']
        if default_date is not None:
            default_date_cls = date.fromisoformat(default_date)
            default_year = f"{default_date_cls.year}"
            default_month = "{:02d}".format(default_date_cls.month)
            default_day = "{:02d}".format(default_date_cls.day)
        else:
            default_year = ""
            default_month = ""
            default_day = ""

        year_question = self.format_question_from_field("--> Année", {'required': True, 'default': default_year, 'type': int})
        month_question = self.format_question_from_field("--> Mois", {'required': True, 'default': default_month, 'type': int})
        day_question = self.format_question_from_field("--> Jour", {'required': True, 'default': default_day, 'type': int})

        year = self.ask(year_question)
        if year == "":
            year = default_year

        month = self.ask(month_question)
        if month == "":
            month = default_month

        day = self.ask(day_question)
        if day == "":
            day = default_day
            

        return "{:02d}-{:02d}-{:02d}".format(int(year), int(month), int(day))

    def asking_for_model(self, model):
        schema = model.get_schema_input()
        print("\n[help]   Obtenir de l'aide\n")
        user_choice = ""
        for field in schema.keys():
            question = self.format_question_from_field(field, schema[field])
            already_asked = False
            while not model.is_valide_field(field) or not already_asked:
                if already_asked:
                    self.print_error(f"Valeur inattendue pour le champ {_t(field)} = {user_choice}")
                current_field = model.get_field(field)
                if current_field['type'] is date:
                    print(self.format_question_from_field(field, current_field))
                    user_choice = self.asking_for_date(current_field)
                else:
                    user_choice = self.ask(question)
                if user_choice == "" and current_field['default'] is not None:
                    user_choice = str(current_field['default'])
                if user_choice == "" and current_field['required']:
                    self.print_error('Ce champ est requis')
                if user_choice.upper() == "/Q":
                        return False
                if user_choice.upper() == "HELP":
                    self.print_help(self.helper_field)
                    continue
                    

                model.set_field_value(field, user_choice)
                already_asked = True
            if user_choice != "":
                choice_value = user_choice
                if current_field['type'] is date:
                    choice_value = self.format_date(user_choice)
                self.print_info(choice_value)
        print('\n')
        return True

    def get_menu_helper(self):
        text = """
        How to use Chess Manager ?
        During your navigation a menu list of actions
        will provide you many choices
        """
        return text

    def print_help(self, text):
        print(_c(f"\n{text}\n", 'yellow'))
        return

    def print_sucess(self, text):
        print(_c(f"\n{text}\n", 'green'))
    
    def print_info(self, text):
        print(_c(f"\n{text}\n", 'blue'))

    def print_error(self, text):
        print(_c(f"\n{text}\n", 'red'))

    def print_table(self, head, body):
        body.insert(0, head)
        table = Table(body)
        print('\n')
        print(table)

    def show_menu(self, actions):
        index = 0
        print("\n")
        for menu_element in actions:
            element_hidden = menu_element[1]
            if not element_hidden:
                element_text = f"[{index}]  {menu_element[0]}"
                element_separator = "-"*(len(element_text) + 5)
                print(element_text)
                index += 1
        print('\n')

    def show(self, actions):
        self.show_menu(actions)
        return self.ask(_c(self.path, 'cyan'), False)

if __name__ == '__main__':

    print()
    print(View.show.__doc__)

