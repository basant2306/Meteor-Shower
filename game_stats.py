class GameStats:

    def __init__(self,ms_game):
        self.settings = ms_game.settings
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):

        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
