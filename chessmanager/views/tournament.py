from chessmanager.views.view import View

from termcolor import colored as _c

from chessmanager.local.local import _t

from datetime import date, datetime

class TournamentView(View):
    def __init__(self, from_path):
        self.from_path = from_path
        self.compute_path()

    def compute_path(self, current_name="Tournoi"):
        self.path =  f"{self.from_path}{current_name}>"

    def compute_age(self, birthday):

        birth_date = date.fromisoformat(birthday)
        birth_year = birth_date.year
        now_date = date.today()
        return (now_date.year - birth_year)

    def show_help(self):
        symbole = _c('*', 'cyan')
        help = [
            "------------------------------------------AIDE TOURNOI------------------------------------\n",
            "Liste des joueur par noms\tAffiche la liste des joueurs inscrit au tournoi\n\t\t\t\ttriée par ordre alphabétique du nom de famille",
            "-------------------------------------------------------------------------------------------",
            "Classement du tournois\t\tAffiche la liste des joueurs inscrit au tournoi\n\t\t\t\ttriée par ordre décroissant des points dans le tournoi",
            "-------------------------------------------------------------------------------------------",
            "Ajouter un joueur\t\tPermet d'inscrire un joueur au tournoi\n\t\t\t\tou de créer un nouveau profil qui\n\t\t\t\tseras ajouté a la liste général",
            "-------------------------------------------------------------------------------------------",
            "Démarer le tournoi\t\tGénere la premiere rondes de matchs",
            "-------------------------------------------------------------------------------------------",
            f"Abréviations {symbole}\t\t\tCT: Classement du Tournoi\n\t\t\t\tCG: Classement Général",
            "-------------------------------------------------------------------------------------------",
            ]
        
        print("\n".join(help))

    def show_players_out_of_tournament(self, available_players, select=False):
        players_index = range(len(available_players))
        head = ['ID', 'Nom', 'Prénom', 'Age', 'CG*']
        players_info = list(map(lambda x, y: [
                str(y),
                x.last_name['value'],
                x.first_name['value'],
                self.compute_age(x.birth_date['value']),
                str(x.rating)
            ], available_players, players_index))
        if len(players_info) > 0:
            if not select:
                head = head[1:]
                players_info = list(map(lambda x: x[1:], players_info))
            self.print_table(head, players_info)

    def show_available_players(self, available_players, select=False, tournament_rating=False):
        players_index = range(len(available_players))
        tournament_players_scores_sorted = sorted(available_players, key=lambda x: x[1], reverse=True)
        tournament_players_rating = [tournament_players_scores_sorted.index(player) + 1 for player in available_players]
        head = ['ID', 'Nom', 'Prénom', 'Age', 'Score', "CG*", "CT*"]
        players_info = list(map(lambda x, y, z: [
                str(y),
                x[0].last_name['value'],
                x[0].first_name['value'],
                self.compute_age(x[0].birth_date['value']),
                str(x[1]),
                str(x[0].rating),
                str(z)
            ], available_players, players_index, tournament_players_rating))
        if len(players_info) > 0:
            if not select:
                head = head[1:]
                players_info = list(map(lambda x: x[1:], players_info))
            if not tournament_rating:
                head = head[:-1]
                players_info = list(map(lambda x: x[:-1], players_info))
            self.print_table(head, players_info)

    def show_available_rounds(self, available_rounds, select=False):
        is_done = False
        rounds_index = range(len(available_rounds))
        head = ['ID', 'Date de début', 'Nb joueurs', 'Nom', 'État', 'Date de fin']
        rounds_info = list(map(lambda x, y: [
                str(y),
                x.start_at.strftime("%d/%m/%Y %H:%M"),
                str(len(x.players)),
                x.name,
                _t(x.state),
                x.end_at.strftime("%d/%m/%Y %H:%M") if type(x.end_at) is datetime else ""
            ], available_rounds, rounds_index))

        if len(rounds_info) > 0:
            if not select:
                head = head[1:]
                rounds_info = list(map(lambda x: x[1:], rounds_info))
            self.print_table(head, rounds_info)

    def show_available_matchs(self, available_matchs):
        matchs_index = range(len(available_matchs))
        head = ['C J1', 'Joueur 1', 'PTS J1', 'PTS J2', 'Joueur 2', 'C J2']
        matchs_info = list(map(lambda x, y: [
                x.colors[0],
                x.player_s1.first_name['value'],
                str(x.score_s1),
                str(x.score_s2),
                x.player_s2.first_name['value'],
                x.colors[1]
            ], available_matchs, matchs_index))

        if len(matchs_info) > 0:

            self.print_table(head, matchs_info)


if __name__ == '__main__':

    print(TournamentView.show.__doc__)

