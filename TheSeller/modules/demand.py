import pygame

class Demand(pygame.sprite.Sprite):
    def __init__(self, position, image, name:str, amount: int, growth: float):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = position)
        self.name = name
        self.position = position
        self.amount = amount
        self.growth = growth