import pygame
import os
from dataclasses import dataclass


@dataclass
class UI:
    def __init__(self):
        self.UISprites = {}
        self.Fonts = {}
        self.Icons = {}
        self.UISpriteFiles = FilesFinder('\\gui\\')
        self.UIFontFiles = FilesFinder('\\font\\')
        self.ActionFiles = FilesFinder('\\actions\\')

    def load_sprites(self):
        self.UISpriteFiles.list_assets()

        for i in range(0, len(self.UISpriteFiles.ListOfFiles)):
            self.UISprites[self.UISpriteFiles.ListOfNames[i]] = pygame.image.load(self.UISpriteFiles.ListOfFiles[i])

    def load_fonts(self):
        self.UIFontFiles.list_assets()

        for i in range(0, len(self.UIFontFiles.ListOfFiles)):
            self.Fonts[self.UIFontFiles.ListOfNames[i]] = self.UIFontFiles.ListOfFiles[i]

    def load_icons(self):
        self.ActionFiles.list_assets()

        for i in range(0, len(self.ActionFiles.ListOfFiles)):
            self.Icons[self.ActionFiles.ListOfNames[i]] = pygame.image.load(self.ActionFiles.ListOfFiles[i])


@dataclass
class FilesFinder:
    def __init__(self, folder: str):
        self.ListOfFiles = []
        self.ListOfNames = []
        self.Folder = f'{os.getcwd()}\\assets' + folder

    def list_assets(self):
        with os.scandir(self.Folder) as directory:
            for dir_entry in directory:
                filename: str = self.__get_filename_from_dir_entry(dir_entry)
                self.ListOfFiles.append(self.Folder + filename)
                self.ListOfNames.append(filename[:-4])

        os.scandir().close()

    def __get_filename_from_dir_entry(self, dir_entry) -> str:
        filename: str = str(dir_entry)[11:-2]

        return filename
