from .menu import Menu
import sys
from termcolor import colored as _c
class View:
   
    def ask(self, question):
        # sys.stdout.write('\x1b[2K\r')
        response_input = input(f"{question} {_c(':', 'yellow')} ")

        return response_input

    def format_question_from_field(self, field_name, field_config):

        field_text = f"{_c(field_name, 'cyan')}{_c('*', 'red')}" if field_config['required'] else _c(field_name, 'cyan')

        if field_config['value'] != "" and field_config['value'] is not None:
            default_value = f"({_c(field_config['value'], 'blue')})"
        else:
            default_value =  ""

        return f"{field_text} {default_value}"

    def asking_for_model(self, model):
        schema = model.get_schema_input()
        print("Les champs* sont requis, (valeur par default)")
        for field in schema.keys():
            question = self.format_question_from_field(field, schema[field])
            already_asked = False
            while not model.is_valide_field(field) or not already_asked:
                user_choice = self.ask(question)
                model.set_field_value(field, user_choice)
                already_asked = True
        return True

        
if __name__ == '__main__':

    print()
    print(View.show.__doc__)