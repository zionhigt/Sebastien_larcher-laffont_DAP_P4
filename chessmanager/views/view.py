from chessmanager.views.table import Table
from chessmanager.local.local import Local

import sys
from termcolor import colored as _c

LOCAL = Local()
_t = LOCAL._t

class View:
    def __init__(self):
        self.exemple_required_with_default = self.format_question_from_field("champ requis",{'required': True,'default': "Valeur par default"})
        self.exemple_required_without_default = self.format_question_from_field("champ requis",{'required': True,'default': ""})
        self.exemple_norequired_without_default = self.format_question_from_field("champ requis",{'required': True,'default': ""})
        self.helper_field = f"""{self.exemple_required_with_default}
                                    {self.exemple_required_without_default}
                                    {self.exemple_norequired_without_default}

                                    [/q]    Annuler l'édition
                                    [help]  Afficher cette aide
                                    """
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
            default_value = f"({_c(field_config['default'], 'yellow')})"
        else:
            default_value =  ""

        return f"{field_text}> {default_value}"

    def asking_for_model(self, model):
        schema = model.get_schema_input()
        print("\n[help]   Obtenir de l'aide\n")
        for field in schema.keys():
            question = self.format_question_from_field(field, schema[field])
            already_asked = False
            while not model.is_valide_field(field) or not already_asked:
                current_field = model.get_field(field)
                user_choice = self.ask(question)
                if user_choice == "" and current_field['default'] != "":
                    user_choice = current_field['default']
                if user_choice is None and current_field['required']:
                    self.print_error('Ce champ est requis')
                if user_choice is not None:
                    if user_choice.upper() == "/Q":
                        return False
                    if user_choice.upper() == "HELP":
                        self.print_help(self.helper_field)
                        continue

                model.set_field_value(field, user_choice)
                already_asked = True
            if user_choice is not None:
                print(f"{_c(user_choice, 'blue')}")
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

    def print_error(self, text):
        print(_c(f"\n{text}\n", 'red'))

    def print_table(self, head, body):
        body.insert(0, head)
        table = Table(body)
        print('\n')
        print(table)
        print('\n')

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
        return self.ask('Que voulez vous faire', False)

if __name__ == '__main__':

    print()
    print(View.show.__doc__)

