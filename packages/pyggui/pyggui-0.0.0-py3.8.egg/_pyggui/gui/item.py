"""
Module containing Item base classes.
"""

from typing import Callable, List, Tuple, Union

import pygame

from pyggui.helpers import create_object_repr


class _Item:
    """
    Base class for all items.
    """
    def __init__(self, position: List[int], size: Tuple[int, int], visible: bool = True, selected: bool = False):
        self.screen = pygame.display.get_surface()

        self.initial_position = position  # Save initial position
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])

        self.items: List[any] = []  # List of items attached to self
        self.visible = visible
        self.selected: bool = selected

    @property
    def position(self) -> List[int]:
        return [self.rect.x, self.rect.y]

    @position.setter
    def position(self, pos: List[int]):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    @property
    def x(self) -> int:
        return self.rect.x

    @x.setter
    def x(self, new_x: int):
        self.rect.x = new_x

    @property
    def y(self) -> int:
        return self.rect.y

    @y.setter
    def y(self, new_y: int):
        self.rect.y = new_y

    @property
    def size(self) -> Tuple[int, int]:
        return self.rect.size

    @size.setter
    def size(self, new_size: Tuple[int, int]):
        self.rect.size = new_size

    @property
    def width(self) -> int:
        return self.rect.width

    @width.setter
    def width(self, new_width: int) -> None:
        self.rect.width = new_width

    @property
    def height(self) -> int:
        return self.rect.height

    @height.setter
    def height(self, new_height: int) -> None:
        self.rect.height = new_height

    def reset_position(self) -> None:
        """
        Method resets items position to its initial one.
        """
        self.position = self.initial_position

    def add_item(self, item: any) -> None:
        """
        Method adds item to self.

        Args:
            item (any): Item to add to self.
        """
        self.items.append(item)

    def __repr__(self) -> str:
        """
        Returns representation of object.
        :return: str representation of object
        """
        return create_object_repr(self)


class Item(_Item):
    def __init__(
        self,
        controller: 'Controller',
        position: List[int] = [0, 0],
        size: Tuple[int, int] = (1, 1),
        on_click: Callable = None,
        movable: bool = False
    ):
        super().__init__(position, size)

        self.controller = controller

        # _on_click is a list of callable functions, where each gets executed once the click event is triggered
        self._on_click: List[Callable] = []
        self.add_on_click(on_click)

        self._last_click_time = 0  # Time of last click
        self.debounce_interval = 150  # Minimum milliseconds passed since last click to accept next click

        # Assign mouse clicked different function, if true -> mouse_clicked() returns true if mouse is pressed
        #                                             else -> mouse_clicked() returns true if mouse clicked
        # Mouse clicked has to be a function so it returns the pointer to the object and not its value
        self.movable = movable
        if self.movable:
            self.debounce_interval = 0
        # Was pressed property used for checking if mouse was pressed on item initially and is still being pressed
        self.was_pressed = False

    @property
    def mouse_clicked(self):
        if self.movable:
            return self.controller.mouse_pressed
        else:
            return self.controller.mouse_clicked

    def add_on_click(self, on_click: Union[Callable, List[Callable], Tuple[Callable]]) -> None:
        """
        Method adds callable function or list of functions to self. These functions get executed once the item
        is clicked.

        Args:
            on_click (Union[Callable, List[Callable], Tuple[Callable]]): Either a callable function or a list / tuple
            of callable functions.
        """
        if isinstance(on_click, (list, tuple)):
            self._on_click += [func for func in on_click]
        else:
            self._on_click.append(on_click)

    def debounce_time(self) -> bool:
        """
        Method checks if enough(debounce_interval) time passed from the time of the last click.
        Used for eliminating double clicks.

        Returns:
            bool: If debounce_interval time has passed or not
        """
        return pygame.time.get_ticks() - self._last_click_time >= self.debounce_interval

    def on_click(self):
        """
        Method gets executed once the item has been clicked on.
        Executes all on_click functions.
        """
        # When mouse clicks on item
        self._last_click_time = pygame.time.get_ticks()
        # Trigger functions
        for func in self._on_click:
            func()

    def update(self):
        """ Used for updating all items attached to it(sizes, positions, etc.). """
        self.hovered = self.rect.collidepoint(self.controller.mouse_position)
        # Check if mouse was clicked on item, in the interval of the debounce time
        if self.hovered and self.mouse_clicked and self.debounce_time():
            self.on_click()
            self.was_pressed = True
        # Mouse was released
        elif not self.mouse_clicked:
            self.was_pressed = False
        # If was pressed and mouse is not on the item anymore still call on_click method works if movable = True
        if self.was_pressed and self.movable:  # Only check if item is movable, otherwise get multiple clicks
            self.on_click()
        # Update all items
        for item in self.items:
            item.update()

    def draw(self):
        """ Used for drawing itself and every item attached to it. """
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            self.rect, width=2
        )
        # Logic for drawing itself goes here
        for item in self.items:
            item.draw()

    def __repr__(self) -> str:
        """
        Returns representation of object.
        :return: str representation of object
        """
        return create_object_repr(self)
