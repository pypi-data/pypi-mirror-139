"""
Module for the Window class which handles everything related to window drawing and updating.
Game wide objects and settings should be set here.
"""

import pygame


class Window:
    """
    Main class for handling everything window related.
    """
    def __init__(self, game: 'Game'):
        """
        Args:
            game (Game): Main Game object used.
        """
        self.game = game
        self.screen = self.game.screen

    def update(self) -> None:
        """
        Method updates and draws the current page while also updating the screen.
        """
        self.screen.fill((0, 0, 0))
        self.game.controller.current_page.update()
        self.game.controller.current_page.draw()
        pygame.display.update()
