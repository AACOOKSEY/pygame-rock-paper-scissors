
class Settings:
    """A class to store the settings for RPS Game."""

    def __init__(self):
        """Initialise the game's static settings."""
        #Screen Settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (100, 100, 100)
    
    def reset_flags(self):
        """Reset all game flags back to their default settings."""
        #Screen Stages
        self.main_menu = False
        self.game_mode_select = False
        self.game_start = False
        self.select_stage = False
        self.fight_stage = False
        self.game_over = False

        #Game Modes
        self.three_mode_active = False
        self.five_mode_active = False
        self.streak_mode_active = False

        self.player_win = False
        self.cpu_win = False