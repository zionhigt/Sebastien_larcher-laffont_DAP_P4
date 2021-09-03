from chessmanager.views.view import View


class RoundView(View):
    def compute_path(self, tournament_name, current_name):
        self.path = f"Chessmanager>Tournois>{tournament_name}>{current_name}>"

    def show_available_matchs(self, available_matchs, select=False):
        matchs_index = range(len(available_matchs))
        head = ['ID', 'C J1', 'Joueur 1', 'PTS J1', 'PTS J2', 'Joueur 2', 'C J2']
        matchs_info = list(map(lambda x, y: [
                str(y),
                x.colors[0],
                x.player_s1.first_name['value'],
                str(x.score_s1),
                str(x.score_s2),
                x.player_s2.first_name['value'],
                x.colors[1]
            ], available_matchs, matchs_index))

        if len(matchs_info) > 0:
            if not select:
                head = head[1:]
                matchs_info = list(map(lambda x: x[1:], matchs_info))
            self.print_table(head, matchs_info)

    def show_match_players(self, available_players):
        players_index = range(len(available_players))
        head = ['ID', 'Prénom', 'Nom']
        players_info = list(map(lambda x, y: [
                str(y),
                x.first_name['value'],
                x.last_name['value']
            ], available_players, players_index))

        if len(players_info) > 0:
            self.print_table(head, players_info)
