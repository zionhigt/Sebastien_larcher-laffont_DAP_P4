from chester.views.table import Table
from chester.local.local import Local

import sys
from termcolor import colored as _c

LOCAL = Local()
_t = LOCAL._t

class View:
    def ask(self, question):
        sys.stdout.write(f"\n{question} {_c(':', 'yellow')} ")
        response_input = input('')
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
        exemple = self.format_question_from_field("champ requis", {'required': True, 'default': "Valeur par default"})
        sys.stdout.write(f"\n{exemple}\n")
        for field in schema.keys():
            question = self.format_question_from_field(field, schema[field])
            already_asked = False
            while not model.is_valide_field(field) or not already_asked:
                current_field = model.get_field(field)
                user_choice = self.ask(question)
                if user_choice == "" and current_field['default'] != "":
                    user_choice = current_field['default']
                if user_choice is None and current_field['required']:
                    sys.stdout.write(f"{_c('Ce champ est requis', 'red')}")
                
                model.set_field_value(field, user_choice)
                already_asked = True
            if user_choice is not None:
                sys.stdout.write(f"{_c(user_choice, 'blue')}")
        return True

        
    def print_table(self, head, body):
        body.insert(0, head)
        table = Table(body)
        sys.stdout.write('\n')
        sys.stdout.write(table.__str__())
        sys.stdout.write('\n')

    def show_menu(self, actions):
        index = 0
        for menu_element in actions:
            element_hidden = menu_element[1]
            if not element_hidden:
                print(f"{index}.\t{menu_element[0]}")
                index += 1
                
    def show(self, actions):
        self.show_menu(actions)
        return self.ask('Que voulez vous faire')

if __name__ == '__main__':

    print()
    print(View.show.__doc__)

