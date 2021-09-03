class RatingCtrl:
    def __init__(self, view, base_ctrl):
        self.base_ctrl = base_ctrl
        self.view = view

    @staticmethod
    def get_players_sorted_by_rate(available_players):
        sorted_player = sorted(available_players, key=lambda x: x.rating)
        return sorted_player

    def set_player_rate(self, player, rate):
        all_players = self.get_players_sorted_by_rate(self.base_ctrl.get_all_players())

        if rate < 1:
            return self.set_player_rate(player, 1)

        if rate in range(len(all_players) + 1):
            player_rating = player.rating

            if rate < player_rating:
                sub_rated_players = all_players[rate - 1:player_rating - 1]
                set_way = 1
            else:
                sub_rated_players = all_players[player_rating:rate]
                set_way = -1

            for sub_rated_player in sub_rated_players:
                sub_rate = sub_rated_player.rating
                sub_rated_player.rating = sub_rate + set_way

            player.rating = rate
        else:
            return self.set_player_rate(player, len(all_players))

    def run(self):
        # TODO
        # Get all players
        # Asking for edit player selctable by id
        # For th selected player aksing for a  new rating
        # If someone had this rating, player level dowgrading for 1 place etc
        # Show new classment

        all_players = self.get_players_sorted_by_rate(self.base_ctrl.get_all_players())
        self.view.show_available_players(all_players)
        player_choiced = self.view.ask("\nEntrez l'ID du joueur")
        if int(player_choiced) in range(len(all_players)):
            player = all_players[int(player_choiced)]

            rate_choiced = self.view.ask(f"\nNouveau classement pour {player.first_name['value']}")
            self.set_player_rate(player, int(rate_choiced))

            self.run()
