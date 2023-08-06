"""
Module containing base classes for pages.
"""

from typing import List, Tuple

import pygame


class Page:
    """
    Main class other pages should inherit from.
    Page object functions similarly to an Item, it can be moved and resized.
    """
    def __init__(self, controller: 'Controller'):
        """
        Args:
            controller (Controller): Main controller object throughout the game.
        """
        self.screen = pygame.display.get_surface()
        self.controller = controller
        self.items = []
        self.items_positions = []  # Positions relative to the top left corner of page
        self.background_color = (0, 0, 0)
        size = self.screen.get_size()
        self.rect = pygame.Rect(0, 0, size[0], size[1])  # Initial position at (0, 0)

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

    def add_item(self, item: any) -> None:
        """
        Method adds item to page. Items position should be set beforehand.

        Args:
            item (any): Item to add to page. Item must have the update and draw methods.
        """
        self.items.append(item)
        self.items_positions.append(item.position)

    def update(self) -> None:
        """
        Method updates every item added to page.
        """
        for i, item in enumerate(self.items):
            x = self.x + self.items_positions[i][0]
            y = self.y + self.items_positions[i][1]
            item.position = [x, y]
            item.update()

    def draw(self) -> None:
        """
        Method draws every item added to page.
        """
        for item in self.items:
            item.draw()
