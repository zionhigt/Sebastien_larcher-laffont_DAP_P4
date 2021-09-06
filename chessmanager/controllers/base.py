from chessmanager.models.player import Player
from chessmanager.models.tournament import Tournament
from chessmanager.models.round import Round


class BaseCtrl:
    def __init__(self):
        self.available_players = []
        self.available_tournament = []

    @staticmethod
    def make_items(model, config):
        for field in config:
            if config[field] != "default":
                value = config[field]
            else:
                value = model.get_field(field)['default']
            model.set_field_value(field, value)
        model.load()
        return

    def deserialize(self):
        players = Player().table.all()
        for player_config in players:
            player_index = self.add_player()
            player = self.get_player_by_index(player_index)
            player.rating = player_config['rating']
            del player_config['rating']
            self.make_items(player, player_config)

        tournaments = Tournament().table.all()
        for tournament_config in tournaments:
            tournament_index = self.add_tournament()
            tournament = self.get_tournament_by_index(tournament_index)
            tournament.players = [
                    [
                        self.get_player_by_info(Player().get_model_by_db_id(player[0])),
                        player[1]
                    ] 
                    for player in tournament_config['players']
                ]
            for t_round_id in tournament_config['rounds']:
                t_round_config = Round().get_model_by_db_id(t_round_id)
                t_round = Round(t_round_config['name'], tournament)
                tournament.add_round(t_round)
                

            tournament.comment = tournament_config['comment']
            tournament.state = tournament_config['state']
            tournament.started = tournament_config['started']
            tournament.ended = tournament_config['ended']
            del tournament_config['rounds']
            del tournament_config['players']
            del tournament_config['comment']
            del tournament_config['state']
            del tournament_config['started']
            del tournament_config['ended']
            self.make_items(tournament, tournament_config)

    def serialize(self):
        
        players = self.get_all_players()
        for player in players:
            player.serialize()
        tournaments = self.get_all_tournament()
        for tournament in tournaments:
            if len(tournament.rounds) == 0:
                tournament.started = False
            for round in tournament.rounds:
                tiny_matchs = []                
                for match in round.matchs:
                    tiny_match = [
                        (match.player_s1.get_db_model_id(), match.score_s1),
                        (match.player_s2.get_db_model_id(), match.score_s2)
                        ]
                    tiny_matchs.append(tiny_match)
                dict_round = round.to_dict()
                dict_round['matchs'] = tiny_matchs
                dict_round['players'] = [player[0].get_db_model_id() for player in dict_round['players']]
                dict_round['orphan_player'] = dict_round['orphan_player'][0].get_db_model_id()
                dict_round['start_at'] = dict_round['start_at']
                if dict_round['end_at'] != "":
                    dict_round['end_at'] = dict_round['end_at']
                del dict_round['tournament']
                print(round.is_serializable())
                round.serialize(dict_round)

            dict_tournament = tournament.to_dict()
            tiny_rounds = [t_round.get_db_model_id() for t_round in tournament.rounds]
            dict_tournament['rounds'] = tiny_rounds
            tiny_t_players = [(player[0].get_db_model_id(), player[1]) for player in tournament.players]
            dict_tournament['players'] = tiny_t_players
            tournament.serialize(dict_tournament)
                

    def add_player(self):

        player = Player()
        self.available_players.append(player)
        return self.available_players.index(player)

    def get_player_by_info(self, info):
        for player in self.available_players:
            if player.first_name['value'] == info['first_name']:
                if player.last_name['value'] == info['last_name']:
                    if player.birth_date['value'] == info['birth_date']:
                        return player
        return None

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
