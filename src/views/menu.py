class Menu:
    def __init__(self, choices_list):
        if(choices_list is None):
            choices_list = {}
        self.choices_list = choices_list

    def show(self):
        for available_choise in self.choices_list.keys():
            key = available_choise
            value = self.choices_list[available_choise]
            print(f"{key}   {value}")

    def asking(self, done, fail):
        self.show()
        user_input = input("Que voulez-vous faire? : ")
        if(user_input in self.choices_list.keys()):
            done(user_input)
        else:
            fail("Cette commande n'existe pas")

