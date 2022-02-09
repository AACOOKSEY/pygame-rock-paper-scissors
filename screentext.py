from typing import Type
import pygame.font

class Screentext:
    """A class to manage miscellaneous on-screen text."""

    def __init__(self, rps_g, template, text, x, y):
        self.screen = rps_g.screen
        self.screen_rect = self.screen.get_rect()
        
        self.settings = rps_g.settings
        
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.x = x
        self.y = y

        #Screentext template
        self.template = template

        #Text properties
        self.font = pygame.font.SysFont(None, 70)
        self.text_colour = (0, 0, 0)

        if self.template == "title":
            self._title_text()
        elif self.template == "info":
            self._info_text()
        elif self.template == "subtitle":
            self._subtitle_text()

        self._prep_text(text)

    def _title_text(self):
        """Template for title text."""
        self.font = pygame.font.SysFont(None, 70)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = 50
    
    def _info_text(self):
        """Template for game mode info text."""
        self.font = pygame.font.SysFont(None, 45)
        self.rect.left = self.x
        self.rect.centery = self.y
        
    def _subtitle_text(self):
        """Template for subtitle text."""
        self.font = pygame.font.SysFont(None, 45)
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def _prep_text(self, text):
        """Turn text into a rendered image."""
        self.text_image = self.font.render(text, True, self.text_colour, 
            self.settings.bg_color)
        self.text_image_rect = self.text_image.get_rect()
        
        if self.template == "title": 
            self.text_image_rect.center = self.rect.center
        elif self.template == "info":
            self.text_image_rect.midleft = self.rect.center
        elif self.template == "subtitle":
            self.text_image_rect.center = self.rect.center

    def draw_text(self):
        """Draw the message onto the screen."""
        self.screen.blit(self.text_image, self.text_image_rect)