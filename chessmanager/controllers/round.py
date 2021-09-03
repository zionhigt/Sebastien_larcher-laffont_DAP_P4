from chessmanager.controllers.ctrl import Ctrl
from chessmanager.controllers.ctrl import compute_available_action
from chessmanager.models.match import Match

from random import randint


class RoundCtrl(Ctrl):
    def __init__(self, view):
        super().__init__(view)
        self.current_round = None
        self.rounds = []
        self.players_in_game = ()

        self.base_actions = [
            ("voir les matchs", False, 'show_matchs'),
            ("Éditer les scores", False, 'edit_scores'),
            ("Terminer la ronde", True, 'mark_as_done'),
            ("Retour", False, 'return')
        ]

        self.action_callback = {
            "show_matchs": self.show_matchs,
            "edit_scores": self.edit_scores_dev,
            "mark_as_done": self.mark_as_done,
            "return": self.exit
        }

    def set_path(self):
        self.view.compute_path(self.current_round.tournament.name['value'], self.current_round.name)

    def mark_as_done(self):
        self.current_round.mark_as_done()
        return

    def edit_scores_dev(self):
        pts = [(1, 0), (0, 1), (0.5, 0.5)]
        for match in self.current_round.matchs:
            pts_index = randint(0, 2)
            match.add_points(pts[pts_index])
            match.played = True
        self.show_available_actions()

    def edit_scores(self):
        self.view.show_available_matchs(self.current_round.matchs, select=True)
        user_choice = self.view.ask("\nEntrez l'ID du match à éditer")
        if int(user_choice) in range(len(self.current_round.matchs)):
            match_to_edit = self.current_round.matchs[int(user_choice)]
            self.view.show_match_players(match_to_edit.players)
            winner = self.view.ask("\nEntrez l'ID du Joueur gagnant ou [null]")
            try:
                if int(winner) in range(2):
                    winner_index = int(winner)
                    points = [0.0, 0.0]
                    points[winner_index] = 1.0
                    match_to_edit.add_points(points)
                    match_to_edit.played = True
                else:
                    self.edit_scores()

            except ValueError:
                if winner.upper() == 'NULL':
                    match_to_edit.add_points([0.5, 0.5])
                    match_to_edit.played = True
                else:
                    self.edit_scores()

            self.view.show_available_matchs([match_to_edit])
        self.show_available_actions()

    def show_matchs(self):
        self.view.show_available_matchs(self.current_round.matchs)
        self.show_available_actions()

    def show_available_actions(self):
        actions_available = self.actions_rules()
        self.show_actions(actions_available, self.action_callback)
        return

    @compute_available_action
    def actions_rules(self):
        """Define what field will be show when round will be loaded"""

        base_actions = list(map(lambda x: list(x), self.base_actions))
        base_actions[2][1] = False
        for match in self.current_round.matchs:
            if not match.played:
                base_actions[2][1] = True
        return base_actions

    def run(self, rounds, persistant=True):
        self.rounds = rounds
        if self.current_round != self.rounds[-1]:
            self.current_round = rounds[-1]
        if not len(self.current_round.matchs):
            first_time = True
            if len(self.rounds) > 1:
                first_time = False
            self.match_making(first_time)
        if persistant:
            self.show_available_actions()

        return

    def add_match(self, player_s1, player_s2):
        match = Match(player_s1, player_s2)
        self.current_round.matchs.append(match)
        return

    def is_already_met(self, player_s1, player_s2):
        rounds_matchs = [match for t_round in self.rounds for match in t_round.matchs]

        all_meetings = [[match.player_s1, match.player_s2] for match in rounds_matchs]

        meeting = [player_s1, player_s2]
        reverse_meeting = list(meeting)
        reverse_meeting.reverse()

        return (meeting in all_meetings) or (reverse_meeting in all_meetings)

    def make_first_match(self):
        players_s1, players_s2 = self.split_players_list()
        for i in range(len(players_s1)):
            j = 0
            player_s1 = players_s1[i]
            player_s2 = players_s2[j]

            while self.is_already_met(player_s1, player_s2):
                j += 1
                if j < len(players_s2) - 1:
                    player_s2 = players_s2[j]
                else:
                    self.view.print_error(
                        " ".join([
                            "Impossible de créer un match,",
                            {player_s1[0].first_name['value']},
                            {player_s1[0].last_name['value']},
                            "à déjà rencontré tout le monde"
                        ]))
                    return

            self.add_match(player_s1, player_s2)
            del players_s2[j]
        return

    def exclude_orphan_player(self, players):
        if len(players) % 2:
            self.current_round.orphan_player = self.current_round.players[-1]
            return players[:-1]
        else:
            return players

    def split_players_list(self):
        players = self.current_round.players
        players = self.exclude_orphan_player(players)
        split_offset = int(len(players)/2)
        self.players_in_game = (players[:split_offset], players[split_offset:])
        return self.players_in_game

    def make_match(self):
        players = [player for player in self.current_round.players]
        players = self.exclude_orphan_player(players)
        while len(players) >= 2:
            j = 1
            player_s1 = players[0]
            player_s2 = players[j]
            while self.is_already_met(player_s1, player_s2):
                j += 1
                player_s2 = players[j]

            self.add_match(player_s1, player_s2)
            del players[j]
            del players[0]

        return

    def match_making(self, first_time):
        if first_time:
            self.make_first_match()
        else:
            self.make_match()

        if self.current_round.orphan_player is not None:
            self.current_round.orphan_player[1] += 1
