import pygame

class Supplies(pygame.sprite.Sprite):
    def __init__(self, position, image, name: str, isSellable: bool, amount: int, production: int, selling: int):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = position)
        self.name = name
        self.position = position
        self.isSellable = isSellable
        self.amount = amount
        self.growth = production
        self.selling = selling