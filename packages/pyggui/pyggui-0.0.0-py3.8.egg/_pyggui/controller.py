"""
Module containing the controller class.

Controller class object acts as an intermediate between game wide objects, used for page redirection, game pausing, ...
"""

from typing import Dict

from pyggui.helpers import Stack
from pyggui.defaults.__welcome_page import _WelcomePage
from pyggui.configure.pages import get_all_page_classes


class Controller:
    """
    Main object throughout the game. Mediator between game object and everything else.
    Contains page_stack attribute which is a Stack, containing visited pages.
    """
    def __init__(self, game: 'Game'):
        """
        Args:
            game (Game): Main game object.
        """
        self.game = game

        # Save as two consecutive mouse positions / clicks, accessible through properties
        self.mouse_position: list[tuple[int, int]] = (0, 0)
        self._mouse_pressed: bool = [False, False]
        self.mouse_clicked = False
        self.mouse_movement = (0, 0)
        self.mouse_scroll = 0  # Wheel on the mouse, 1 if up -1 if down roll
        self.esc_clicked: bool = False
        self.key_pressed: dict = {}
        # Pages setup
        self.pages: Dict = get_all_page_classes()
        self.page_stack: Stack = Stack()
        # Landing page setup
        # If no page was found or the default entry was left as is -> add the welcome_page from defaults
        if not bool(self.pages) or self.game.entry_page == "_WelcomePage":
            self.pages["_WelcomePage"] = _WelcomePage
            self.current_page = _WelcomePage
        else:
            self.current_page = self.pages[self.game.entry_page]

    @property
    def mouse_pressed(self) -> bool:
        """
        If mouse was clicked on current frame.

        Returns:
            bool: If clicked
        """
        return self._mouse_pressed[-1]  # Last click

    @mouse_pressed.setter
    def mouse_pressed(self, clicked: bool) -> None:
        """
        Mouse pressed on current frame.

        Args:
            clicked (bool): If mouse pressed
        """
        self._mouse_pressed.append(clicked)
        self._mouse_pressed = self._mouse_pressed[-2:]  # Save as only the last 2 recent clicks

    @property
    def previous_mouse_pressed(self) -> bool:
        """
        If mouse was pressed on previous frame.

        Returns:
            bool: If pressed
        """
        return self._mouse_pressed[0]  # Left one is the previous one as we append clicks

    @property
    def dt(self) -> float:
        """
        Difference in time (milliseconds) between current frame and previous frame.

        Returns:
            float: Milliseconds
        """
        return self.game.dt

    @property
    def dt_s(self) -> float:
        """
        Difference in time (seconds) between current frame and previous frame.

        Returns:
            float: Seconds
        """
        return self.game.dt_s

    @property
    def paused(self) -> bool:
        """
        If game is currently paused.

        Returns:
            bool: If paused
        """
        return self.game.paused

    @property
    def current_page(self) -> any:
        """
        Current page on top of the page stack.

        Returns:
            any: Page
        """
        return self.page_stack.peak()

    @current_page.setter
    def current_page(self, page: any) -> None:
        """
        Set current page to be on top of stack.

        Args:
            page (any): Page to push on top of stack.
        """
        self.page_stack.push(page(self))  # Initialize page

    def redirect_to_page(self, to_page: str, *args, **kwargs) -> None:
        """
        Method redirects to page defined as a string. Args and Kwargs are passed to page class initialization.
        Error gets displayed if page does not exist. TODO: Make custom error

        Args:
            to_page (str): Page to redirect to, has to be defined in the pages dictionary.
            *args (any): Get passed to pages class initialization.
            **kwargs (any): Get passed to pages class initialization.
        """
        if to_page in self.pages.keys():
            self.page_stack.push(self.pages[to_page](self, *args, **kwargs))  # Initialize page and push on stack
        else:
            print(f"Controller: Redirection error to page {to_page}. Page does not exist.")

    def go_back(self) -> None:
        """
        Method goes back one page in the page stack.
        """
        if not self.page_stack.empty():
            self.page_stack.pop()
        else:
            print(f"Controller: Redirection error calling go_back.\n   Page stack is empty.")

    def pause_game(self) -> None:
        """
        Method pauses and un-pauses game.
        """
        self.game.paused = not self.game.paused
