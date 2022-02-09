import sys
import pygame
import json

from random import randint

from screentext import Screentext
from settings import Settings
from game_stats import GameStats
from button import Button
from screentext import Screentext
from paper import Paper
from rock import Rock
from scissors import Scissors

class RPS:
    """Overall class to manage game."""
    
    def __init__(self):
        """Initialise the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats()

        #Set up the game screen.
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Rock, Paper, Scissors!")
        self.screen_rect = self.screen.get_rect()

        self.paper = Paper(self)
        self.rock = Rock(self)
        self.scissors = Scissors(self)

        self.filename = 'score.json'
        with open(self.filename) as self.f:
            self.scores = json.load(self.f)

    def run_game(self):
        """Start and run the main game loop."""
        self.settings.reset_flags()
        self._main_menu()
        while True:
            self.mouse_pos = pygame.mouse.get_pos()
            self._check_events()
            self._update_screen()

    def _reset_game(self):
        """Reset the game stats and flags back to their default"""
        self.stats.reset_stats()
        self.settings.reset_flags()

    def _main_menu(self):
        """Create the main menu."""
        self._reset_game()
        self.settings.main_menu = True

        #Text
        self.title_text = Screentext(self, "title","Rock, Paper, Scissors!",
            self.screen_rect.centerx, 50)

        #Buttons
        self.mm_play_button = Button(self, "Play",
            self.screen_rect.centerx - 75,
            self.screen_rect.centery - 75)
        self.mm_quit_button = Button(self, "Quit",
            self.mm_play_button.rect.x, 
            self.mm_play_button.rect.y + 150)

    def _game_mode_select(self):
        """Create the game mode selection menu."""
        #Title Text
        self.game_mode_text = Screentext(self, "title","Select a Game Mode",
            self.screen_rect.centerx, 50)

        #Buttons
        self.gm_three_button = Button(self, "Three", 100, 200)
        self.gm_five_button = Button(self, "Five",
            self.gm_three_button.rect.x,
            self.gm_three_button.rect.y + 100)
        self.gm_streak_button = Button(self, "Streak",
            self.gm_three_button.rect.x,
            self.gm_five_button.rect.y + 100)
        self.gm_back_button = Button(self, "Back",
            self.gm_three_button.rect.x,
            self.gm_streak_button.rect.y + 100)

        #Info Text
        self.gm_three_text = Screentext(self, "info",
            "First to Three Wins", 
            (self.gm_three_button.rect.height + 200),
            (self.gm_three_button.rect.centery))  
        self.gm_five_text = Screentext(self, "info",
            "First to Five Wins", 
            (self.gm_five_button.rect.height + 200),
            (self.gm_five_button.rect.centery))  
        self.gm_streak_text = Screentext(self, "info",
            "Keep Going Until You Lose!",
            (self.gm_streak_button.rect.height + 200),
            (self.gm_streak_button.rect.centery))  

    def _game_start(self):
        self.player_choice = 0
        self.cpu_choice = 0
        
        if self.settings.three_mode_active == True:
            self._three_mode()
        elif self.settings.five_mode_active == True:
            self._five_mode()
        elif self.settings.streak_mode_active == True:
            self._streak_mode()

    def _three_mode(self):
        """Set up the first to three wins game mode."""
        self.gs_title_text = Screentext(self, "title", "First to Three!",
            self.screen_rect.centerx, 50)
        self.gs_score_text = Screentext(self, "subtitle", 
            f"YOU {self.stats.pc_score} - {self.stats.cpu_score} CPU",
            self.screen_rect.centerx, 100)
        
        self.gamemode = "three"
        self.score_limit = 3
        self._player_select_weapon()

    def _five_mode(self):
        """Set up the first to five wins game mode."""
        self.gs_title_text = Screentext(self, "title", "First to Five!",
            self.screen_rect.centerx, 50)
        self.gs_score_text = Screentext(self, "subtitle", 
            f"YOU {self.stats.pc_score} - {self.stats.cpu_score} CPU",
            self.screen_rect.centerx, 100)
        
        self.gamemode = "five"
        self.score_limit = 5
        self._player_select_weapon()
    
    def _streak_mode(self):
        """Set up the streak game mode."""
        self.gs_title_text = Screentext(self, "title", 
        "Streak Mode! Keep going 'til you lose!", 
        self.screen_rect.centerx, 50)
        self.gs_score_text = Screentext(self, "subtitle", 
            f"Current Streak: {self.stats.pc_score}",
            self.screen_rect.centerx, 100)

        self.score_limit = 1
        self._player_select_weapon()        

    def _player_select_weapon(self):
        """Asks for user's weapon choice."""
        
        if self.player_choice == 0:
            self.settings.select_stage = True
        elif self.player_choice == 1:
            self.player_choice_name = "Rock"
            self.settings.select_stage = False
            self._cpu_select_weapon()
        elif self.player_choice == 2:
            self.player_choice_name = "Paper"
            self.settings.select_stage = False
            self._cpu_select_weapon()
        elif self.player_choice == 3:
            self.player_choice_name = "Scissors"
            self.settings.select_stage = False
            self._cpu_select_weapon()

    def _cpu_select_weapon(self):
        """Generates the computer's weapon choice."""
        self.cpu_choice = randint(1,3)
        self.settings.fight_stage = True

        if self.cpu_choice == 1:
            self.cpu_choice_name = "Rock"
        elif self.cpu_choice == 2:
            self.cpu_choice_name = "Paper"
        elif self.cpu_choice == 3:
            self.cpu_choice_name = "Scissors"

        self.player_choice_text = Screentext(self, "subtitle", 
            f"You picked {self.player_choice_name}.",
            self.screen_rect.centerx, 200)
        self.cpu_choice_text = Screentext(self, "subtitle", 
            f"CPU picked {self.cpu_choice_name}.",
            self.screen_rect.centerx, 300)

    def _check_weapons(self):
        """Checks the player's and computer's weapons and updates the score"""
        if self.player_choice == self.cpu_choice:
            self.round_result = "It's a tie!"
        #Player picks Rock
        elif self.player_choice == 1:
            #CPU picks Paper
            if self.cpu_choice == 2:
                self.stats.cpu_score += 1
                self.round_result = "CPU wins the round."
            #CPU picks Scissors
            elif self.cpu_choice == 3:
                self.stats.pc_score += 1
                self.round_result = "You win the round."
        
        #Player picks Paper
        elif self.player_choice == 2:
            #CPU picks Rock
            if self.cpu_choice == 1:
                self.stats.pc_score += 1
                self.round_result = "You win the round."
            #CPU picks Scissors
            elif self.cpu_choice == 3:
                self.stats.cpu_score += 1
                self.round_result = "CPU wins the round."
        
        #Player picks Scissors
        elif self.player_choice == 3:
            #CPU picks Rock
            if self.cpu_choice == 1:
                self.stats.pc_score += 1
                self.round_result = "You win the round."
            #CPU picks Paper
            elif self.cpu_choice == 2:
                self.stats.cpu_score += 1
                self.round_result = "CPU wins the round."

        self.round_result_text = Screentext(self, "subtitle", 
            self.round_result,
            self.screen_rect.centerx, 400)
        
        self.next_button = Button(self, "Next", 
            (self.screen_rect.centerx - 75),
            (self.round_result_text.rect.y + 200))

    def _game_over_screen(self):
        """Screen to render once player wins or loses."""
        self.gos_title_text = Screentext(self, "title", "GAME OVER!", 
            self.screen_rect.centerx, 50)
        
        if self.settings.streak_mode_active == True:
            self.winner = f"""You ended with a streak of
            {self.stats.pc_score} wins!"""
        elif self.settings.player_win == True:
            self.winner = "You win!"
        elif self.settings.cpu_win == True:
            self.winner = "You lose!"

        if self.settings.three_mode_active == True:
            self.scoretext = f"Current Record: W {self.scores['three_wins']}"
            self.scoretext += f" - {self.scores['three_losses']} L."
        elif self.settings.five_mode_active == True:
            self.scoretext = f"Current Record: W {self.scores['five_wins']}"
            self.scoretext += f"- {self.scores['five_losses']} L."
        elif self.settings.streak_mode_active == True:
            self.scoretext = f"""Highest Streak: 
            {self.scores['streak_highscore']} wins."""

        self.gos_result_text = Screentext(self, "subtitle", self.winner,
            self.screen_rect.centerx, self.gos_title_text.rect.y + 100)
        
        self.gos_highscore_text = Screentext(self, "subtitle", self.scoretext,
            self.screen_rect.centerx, self.gos_result_text.rect.y + 75)

        self.gos_replay_text = Screentext(self, "subtitle", 
            "Would you like to play again?", self.screen_rect.centerx, 
            self.gos_highscore_text.rect.y + 75)
        
        self.gos_replay_button = Button(self, "Replay", 
            self.screen_rect.centerx - 75,
            self.gos_replay_text.rect.y + 100)
        
        self.gos_menu_button = Button(self, "Menu", 
            self.screen_rect.centerx - 75,
            self.gos_replay_button.rect.y + 100)
            

    def _check_events(self):
        """Respond to mouse movement and clicks."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_buttons(self.mouse_pos)

    def _check_buttons(self, mouse_pos):
        """Check for mouse-button interactions."""
        mouse_pos = self.mouse_pos
        
        #Main Menu Buttons
        if self.settings.main_menu == True:
            if self.mm_play_button.rect.collidepoint(mouse_pos):
                self._game_mode_select()
                self.settings.main_menu = False
                self.settings.game_mode_select = True
            elif self.mm_quit_button.rect.collidepoint(mouse_pos):
                sys.exit()
        
        #Game Mode Select Buttons
        if self.settings.game_mode_select == True:
            if self.gm_three_button.rect.collidepoint(mouse_pos):
                self.settings.game_mode_select = False
                self.settings.game_start = True
                self.settings.three_mode_active = True
                self._game_start()
            elif self.gm_five_button.rect.collidepoint(mouse_pos):
                self.settings.game_mode_select = False
                self.settings.game_start = True
                self.settings.five_mode_active = True
                self._game_start()
            elif self.gm_streak_button.rect.collidepoint(mouse_pos):
                self.settings.game_mode_select = False
                self.settings.game_start = True
                self.settings.streak_mode_active = True
                self._game_start()
            if self.gm_back_button.rect.collidepoint(mouse_pos):
                self.settings.main_menu = True
                self.settings.game_mode_select = False
                self._main_menu()
        
        #Game Start Buttons
        if self.settings.select_stage == True:
            if self.rock.rect.collidepoint(mouse_pos):
                self.player_choice = 1
                self._player_select_weapon()
                self._check_weapons()
            elif self.paper.rect.collidepoint(mouse_pos):
                self.player_choice = 2
                self._player_select_weapon()
                self._check_weapons()
            elif self.scissors.rect.collidepoint(mouse_pos):
                self.player_choice = 3
                self._player_select_weapon()
                self._check_weapons()
            
        if self.settings.fight_stage == True:
            if self.next_button.rect.collidepoint(mouse_pos):
                if self.settings.streak_mode_active == True:
                    if self.stats.cpu_score == self.score_limit:
                        self.settings.fight_stage = False
                        self.settings.game_start = False
                        self.settings.game_over = True

                        if self.scores['streak_highscore'] < self.stats.pc_score:
                            self.scores['streak_highscore'] = self.stats.pc_score
                            with open(self.filename, 'w') as f:
                                json.dump(self.scores, f)

                        self._game_over_screen()
                    else:
                        self.player_choice = 0
                        self._player_select_weapon()                      
                else:
                    if self.stats.pc_score == self.score_limit:
                        self.settings.player_win = True
                        self.settings.fight_stage = False
                        self.settings.game_start = False
                        self.settings.game_over = True

                        self.scores[f'{self.gamemode}_wins'] += 1
                        with open(self.filename, 'w') as f:
                            json.dump(self.scores, f)

                        self._game_over_screen()
                    elif self.stats.cpu_score == self.score_limit:
                        self.settings.cpu_win = True
                        self.settings.fight_stage = False
                        self.settings.game_start = False
                        self.settings.game_over = True

                        self.scores[f'{self.gamemode}_losses'] += 1
                        with open(self.filename, 'w') as f:
                            json.dump(self.scores, f)

                        self._game_over_screen()
                    else:
                        self.player_choice = 0
                        self._player_select_weapon()
        
        if self.settings.game_over == True:
            if self.gos_replay_button.rect.collidepoint(mouse_pos):
                if self.settings.three_mode_active == True:
                    self._reset_game()
                    self.settings.three_mode_active = True
                elif self.settings.five_mode_active == True:
                    self._reset_game()
                    self.settings.five_mode_active = True
                elif self.settings.streak_mode_active == True:
                    self._reset_game()
                    self.settings.streak_mode_active = True
                self.settings.game_mode_select = False
                self.settings.game_start = True
                self._game_start()                
            elif self.gos_menu_button.rect.collidepoint(mouse_pos):
                self._main_menu()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        #Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        if self.settings.main_menu == True:
            self.title_text.draw_text()
            self.mm_play_button.draw_button()
            self.mm_quit_button.draw_button()

        elif self.settings.game_mode_select == True:
            self.game_mode_text.draw_text()
            self.gm_three_text.draw_text()
            self.gm_five_text.draw_text()
            self.gm_streak_text.draw_text()

            self.gm_three_button.draw_button()
            self.gm_five_button.draw_button()
            self.gm_streak_button.draw_button()
            self.gm_back_button.draw_button()

        elif self.settings.game_start == True:
            self.gs_title_text.draw_text()
            self.gs_score_text.draw_text()
            if self.settings.select_stage == True:
                self.paper.blitme()
                self.rock.blitme()
                self.scissors.blitme()
            elif self.settings.fight_stage == True:
                self.player_choice_text.draw_text()
                self.cpu_choice_text.draw_text()
                self.round_result_text.draw_text()
                
                if self.settings.streak_mode_active == True:
                    self.gs_score_text._prep_text(
                        f"Current Streak: {self.stats.pc_score}")
                else:
                    self.gs_score_text._prep_text(
                        f"YOU {self.stats.pc_score} - {self.stats.cpu_score} CPU")
                
                self.gs_score_text.draw_text()

                self.next_button.draw_button()
        
        elif self.settings.game_over == True:
            self.gos_title_text.draw_text()
            self.gos_result_text.draw_text()
            self.gos_highscore_text.draw_text()
            self.gos_replay_text.draw_text()

            self.gos_replay_button.draw_button()
            self.gos_menu_button.draw_button()

        #Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    rps = RPS()
    rps.run_game()