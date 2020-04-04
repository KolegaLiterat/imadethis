#libs
import os
import pygame
from typing import List


class Sprites(pygame.sprite.Sprite):
#public
    loaded_sprites = []
#private
    __png_assets: List[str] = []

#public
    def load_sprites(self):
        self.__list_image_assets()

        for png_graphic in self.__png_assets:
            SPRITE = pygame.image.load(os.path.join('./assets/', png_graphic))

            self.loaded_sprites.append(SPRITE)

#private
    def __list_image_assets(self):
        with os.scandir('./assets/') as iterator:
            for file in iterator:
                if not file.name.startswith('.') and file.is_file():
                    file = self.__create_str_from_direntry(file)
                    self.__png_assets.append(file)
        
        os.scandir().close()
    
    def __create_str_from_direntry(self, dir_entry):
        casted_dir_entry: str = str(dir_entry)
        casted_dir_entry = casted_dir_entry[11:-2]

        return casted_dir_entry
