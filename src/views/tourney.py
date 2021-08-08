from datetime import date
from .view import View

class TourneyView(View):

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
    print(TourneyView.show.__doc__)