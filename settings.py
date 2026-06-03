class Settings:
    def __init__(self):
        
        self.screen_width = 1000
        self.screen_height = 500
        self.fullscreen=True
        self.bg_color = (230,230,230)
        self.ship_limit = 3
        self.bullets_allowed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):

        self.ship_speed = 6.5
        self.bullet_speed = 4.5
        self.meteor_speed = 3.0
        self.meteor_points = 10
        self.meteor_spawn_delay = 1000
        self.min_spawn_delay = 800
        self.max_spawn_delay = 2000
        self.max_meteors = 8

    def increase_speed(self):

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.meteor_speed *= self.speedup_scale
        self.meteor_points = int(self.meteor_points * self.score_scale)
        self.min_spawn_delay = max(300, self.min_spawn_delay - 100)
        self.max_spawn_delay = max(600, self.max_spawn_delay - 100)
        self.max_meteors = min(15, self.max_meteors + 1)


        
