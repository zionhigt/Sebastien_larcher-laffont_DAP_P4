from chessmanager.models.player import Player
from chessmanager.models.tournament import Tournament
from chessmanager.models.round import Round
from chessmanager.models.match import Match

from chessmanager.views.view import View

from datetime import datetime
from os import path, system
from tinydb import TinyDB


class BaseCtrl:
    def __init__(self):
        self.view = View()
        self.available_players = []
        self.available_tournament = []
        data_folder = '.\data'
        database_folder = path.join(data_folder, 'database')
        if not path.isdir(data_folder):
            system(f"mkdir {data_folder}")
            system(f"mkdir {database_folder}")

        self.db_path = path.join(database_folder, "chess_db_save.json")

        self.DB = TinyDB(self.db_path)

    def add_player(self):

        player = Player()
        self.available_players.append(player)
        player.rating = len(self.available_players)
        return self.available_players.index(player)

    def get_player_by_index(self, index):

        return self.available_players[index]

    def delete_player_by_index(self, index):
        if len(self.available_players) > index:
            del self.available_players[index]

    def get_all_players(self):

        return self.available_players

    def add_tournament(self):

        tournament = Tournament()
        self.available_tournament.append(tournament)

        return self.available_tournament.index(tournament)

    def get_tournament_by_index(self, index):

        return self.available_tournament[index]

    def get_all_tournament(self):

        return self.available_tournament

    def delete_tournament_by_index(self, index):
        if len(self.available_tournament) > index:
            del self.available_tournament[index]

    def save(self):
        players_table = self.DB.table("Players")
        tournaments_table = self.DB.table('Tournaments')
        players_table.truncate()
        tournaments_table.truncate()

        tiny_player = {
            "last_name": "",
            "first_name": "",
            "birth_date": 0
        }

        tiny_tournament = {
            'name': "",
            'at_date': 0,
            'at_place': "",
            'turns': 0,
            'time_handler': "",
            'comment': "",
            "state": "",
            "started": "",
            "ended": "",
            "players": [],
            "rounds": []
        }

        tiny_round = {
            "name": "",
            "matchs": [],
            "start_at": "",
            "end_at": "",
            "state": ""
        }

        tiny_match = {
            "player_s1": 0,
            "player_s2": 1,
            "score_s1": 0,
            "score_s2": 0,
            "colors_s1": "",
            "colors_s2": "",
            "played": False
        }
        for player in self.available_players:
            ser_player = dict(tiny_player)
            ser_player.update({
                "last_name": player.last_name['value'],
                "first_name": player.first_name['value'],
                "birth_date": player.birth_date['value']
            })
            players_table.insert(ser_player)

        for tournament in self.available_tournament:
            ser_tournament = dict(tiny_tournament)
            t_players = [[self.available_players.index(player[0]), player[1]] for player in tournament.players]
            t_rounds = []
            for t_round in tournament.rounds:
                round_matchs = []
                for match in t_round.matchs:
                    ser_match = dict(tiny_match)
                    ser_match.update({
                        "player_s1": self.available_players.index(match.player_s1),
                        "player_s2": self.available_players.index(match.player_s2),
                        "score_s1": match.score_s1,
                        "score_s2": match.score_s2,
                        "colors_s1": match.colors[0],
                        "colors_s2": match.colors[1],
                        "played": match.played
                    })
                    round_matchs.append(ser_match)

                ser_round = dict(tiny_round)
                end_at = ""
                if t_round.end_at != "":
                    end_at = t_round.end_at.timestamp()
                ser_round.update({
                    "name": t_round.name,
                    "matchs": round_matchs,
                    "start_at": t_round.start_at.timestamp(),
                    "end_at": end_at,
                    "state": t_round.state
                })

                t_rounds.append(ser_round)

            ser_tournament.update({
                'name': tournament.name['value'],
                'at_date': tournament.at_date['value'],
                'at_place': tournament.at_place['value'],
                'turns': tournament.turns['value'],
                'time_handler': tournament.time_handler['value'],
                'comment': tournament.comment['value'],
                'state': tournament.state,
                'started': tournament.started,
                'ended': tournament.ended,
                'players': t_players,
                'rounds': t_rounds
            })
            tournaments_table.insert(ser_tournament)

            self.view.print_sucess("Partie sauvegardée avec succés")

    @staticmethod
    def make_items(model, config):
        for field in config:
            if config[field] != "default":
                value = config[field]
            else:
                value = model.get_field(field)['default']
            model.set_field_value(field, value)
        model.load()

    def load(self):
        players_table = self.DB.table("Players")
        tournaments_table = self.DB.table('Tournaments')

        tiny_players = players_table.all()
        tiny_tournaments = tournaments_table.all()

        for player_config in tiny_players:
            player_index = self.add_player()
            player = self.get_player_by_index(player_index)
            self.make_items(player, player_config)

        for tournament_config in tiny_tournaments:
            item_config = {
                'name': tournament_config['name'],
                'at_date': tournament_config['at_date'],
                'at_place': tournament_config['at_place'],
                'turns': tournament_config['turns'],
                'time_handler': tournament_config['time_handler'],
                'comment': tournament_config['comment'],
            }
            tournament_index = self.add_tournament()
            tournament = self.get_tournament_by_index(tournament_index)
            self.make_items(tournament, item_config)
            tournament.players = [
                [self.get_player_by_index(index_player), score_player]
                for index_player, score_player in tournament_config['players']
                ]
            rounds = []
            for t_round in tournament_config['rounds']:
                round = Round(t_round['name'], tournament)
                matchs = []
                for round_match in t_round['matchs']:
                    match_player_s1 = [self.get_player_by_index(round_match['player_s1'])]
                    match_player_s2 = [self.get_player_by_index(round_match['player_s2'])]
                    match = Match(match_player_s1, match_player_s2)
                    match.score_s1 = round_match['score_s1']
                    match.score_s2 = round_match['score_s2']
                    match.colors = [round_match['colors_s1'], round_match['colors_s2']]
                    match.played = round_match['played']
                    matchs.append(match)

                round.matchs = matchs
                round.players = tournament.players
                round.state = t_round['state']
                round.start_at = datetime.fromtimestamp(t_round['start_at'])
                end_at = ""
                if t_round['end_at'] != "":
                    end_at = datetime.fromtimestamp(t_round['end_at'])
                round.end_at = end_at

                rounds.append(round)

            tournament.rounds = rounds
            tournament.state = tournament_config['state']
            tournament.started = tournament_config['started']
            tournament.ended = tournament_config['ended']

            self.view.print_sucess("Partie chargée avec succés")
