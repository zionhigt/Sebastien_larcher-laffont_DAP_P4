class Local:
    def __init__(self, local='fr'):
        self.local = local
        self.translator = {
            'fr': {
                'at_date': 'Date',
                'birth_date': 'Date de naissance',
                'at_place': 'Lieu',
                'name': 'Nom',
                'last_name': 'Nom',
                'first_name': 'Prénom',
                'score': 'Score',
                'rating': 'Rang',
                'rate': 'Rang',
                'comment': 'Description',
                'time_handler': 'Contrôleur de temps',
                'turns': 'Nombre de tours',
                'DONE': 'Terminé.e',
                'PROCESS': 'En cours',
                'AWAIT': 'En attente'
            }
        }

    def t(self, key):
        try:
            return self.translator[self.local][key]
        except KeyError:
            return key


t = Local().t
