from typing import Any
import pygame.sprite as sprite
import pygame
from pygame.sprite import AbstractGroup
from . import display
sprite_group = sprite.OrderedUpdates()

class Sprite(sprite.Sprite):
    def __init__(self, surface, image, rectangle, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.surf: pygame.Surface = surface
        self.image = display.loadImage(image)
        self.rect = Rect(rectangle)
        self.angle = 0
        self.position = pygame.Vector2(self.rect[:2])
    def move(self, x_position, y_position):
        self.position = pygame.Vector2()
        self.rect.move_ip(x_position, y_position)
    def rotate(self, angle_delta):
        self.angle += angle_delta
    def push(self, velocity):
        self.position += pygame.Vector2(velocity).rotate(self.angle)