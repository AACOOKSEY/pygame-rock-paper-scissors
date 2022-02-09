import pygame.font

class Button:
    """A class to establish miscellaneous buttons."""

    def __init__(self, rps_g, message, x, y):
        self.button_highlight = False
        self.screen = rps_g.screen
        self.screen_rect = self.screen.get_rect()

        #Size
        self.width = 150
        self.height = 75

        #Color
        self.button_color = (25, 25, 25)
        
        #Text properties
        self.font = pygame.font.SysFont(None, 52)
        self.text_color = (230, 230, 230)
        self.message = message

        #Build rect and establish position
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = x
        self.rect.y = y

        #
        self._prep_msg(message)

    def _prep_msg(self, message):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(message, True, self.text_color, 
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.button_highlight = True
            self.highlight(self.message)
        else:
            self.button_highlight = False
            self.highlight(self.message)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def highlight(self, message):
        """Highlight the button on mouseover."""
        if self.button_highlight == True:
            self.button_color = (230, 230, 230)
            self.text_color = (25, 25, 25)
        else:
            self.button_color = (25, 25, 25)
            self.text_color = (230, 230, 230)
        self._prep_msg(message)