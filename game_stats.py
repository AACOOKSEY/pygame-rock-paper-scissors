
class GameStats:
    """A class to track player statistics."""
    
    def __init__(self):
        """Initialise statistics."""
        self.reset_stats()

        #Start game in inactive state.
        self.game_active = False

        #High scores
        self.three_wins = 0
        self.three_losses = 0

        self.five_wins = 0
        self.five_losses = 0
        
        self.streak_highscore = 0

    def reset_stats(self):
        """Initialise dynamic statistics."""
        self.pc_score = 0
        self.cpu_score = 0