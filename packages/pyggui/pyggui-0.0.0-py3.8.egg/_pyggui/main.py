"""
Module containing main Game class
"""

from typing import Tuple
import inspect

import pygame

from pyggui.controller import Controller
from pyggui.input import Input
from pyggui.window import Window
from pyggui import configure


class Game:
    """
    Main class for game, holds every game wide property, setting and the main run loop.
    """
    def __init__(
        self,
        display_size: Tuple[int, int] = (720, 360),
        page_directory: str = None,
        entry_page: str = "_WelcomePage",
        fps: int = 0
    ):
        """
        Args:
            display_size (Tuple[int, int]): Size of display in px. Defaults to (720, 360).
            page_directory (str): Absolute or relative path to directory containing pages.
                Defaults to directory of where this object is initialised.
            fps (int): Fps constant for game loop.
        """
        # Import all modules containing pages
        configure.pages.setup(inspect.stack()[1], directory=page_directory)
        # Pygame initial configuration
        pygame.init()
        self.screen = pygame.display.set_mode(display_size)
        pygame.display.set_caption("Pygame Window w/pyggui")
        self.clock = pygame.time.Clock()
        # Attributes
        self._fps = fps
        self._dt = 0  # Change of time between seconds
        self.paused = False  # If game is paused
        self.entry_page = entry_page
        # Game wide objects
        self.development = None  # Development(self)
        self.controller = Controller(self)
        self.window = Window(self)
        self.input = Input(self)

    @property
    def dt(self) -> float:
        """
        Difference in time (milliseconds) between current frame and previous frame.
        """
        return self._dt

    @property
    def dt_s(self) -> float:
        """
        Difference in time (seconds) between current frame and previous frame.
        """
        return self._dt * 0.001

    @property
    def fps(self) -> float:
        """
        Current FPS the game is running at.
        """
        return round(1000 / self._dt)

    @fps.setter
    def fps(self, frame_rate: int) -> None:
        """
        Cap FPS of game at given integer value.
        """
        self._fps = int(frame_rate)

    def run(self) -> None:
        """
        Run main game loop. Will update Window, Input and grab time passed from previous frame.
        Loop ends if Input.update returns False i.e. a quit event appeared.
        """
        running = True
        while running:
            self.window.update()
            running = self.input.update()
            self._dt = self.clock.tick(self._fps)
