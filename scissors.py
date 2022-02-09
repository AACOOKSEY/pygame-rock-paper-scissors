import pygame

class Scissors:
    "A class representing the Scissors image and button."
    def __init__(self, rps_g):
        """Initialise Scissors attributes."""
        self.screen = rps_g.screen
        self.screen_rect = self.screen.get_rect()

        #Load image
        self.image = pygame.image.load('images/scissors.bmp')
        self.rect = self.image.get_rect()

        #Position image
        self.rect.center = self.screen_rect.center
        self.rect.x += 150

        self.scissors_highlight = False

    def blitme(self):
        """Draw the image at its current location."""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.highlight()
            self.scissors_highlight = True
        self.screen.blit(self.image, self.rect)
    
    def highlight(self):
        """Highlight the image on mouseover."""
        pygame.draw.rect(self.screen, (255, 255, 255),
        (self.rect.left - 5, self.rect.top - 5, 110, 110))