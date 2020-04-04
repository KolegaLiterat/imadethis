import pygame

class Workers(pygame.sprite.Sprite):
    def __init__(self, position, image, isIdle: bool):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = position)
        self.position = position 
        self.isIdle = isIdle