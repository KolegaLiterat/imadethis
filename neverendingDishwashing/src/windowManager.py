import pygame
from dataclasses import dataclass
from typing import List, Tuple, Union


@dataclass
class GameWindow:
    def __init__(self, size: Tuple[int, int]):
        self.Width = size[0]
        self.Height = size[1]

    def create_window(self) -> Union[pygame.Surface, pygame.SurfaceType]:
        window: Union[pygame.Surface, pygame.SurfaceType] = pygame.display.set_mode((self.Width, self.Height))

        return window


@dataclass
class GameSurface:
    def __init__(self):
        self.Surfaces = {}
        self.SurfacesNames: List[str] = ['DishBar', 'PlayerBar', 'Dish0', 'Dish1', 'PlayerActions',
                                         'PlayerAction0', 'PlayerAction1', 'PlayerAction2', 'DirtyDishes', 'CleanDishes']

    def create_surface(self):
        surfaces_sizes: List[Tuple[int, int]] = [(600, 70), (600, 70), (64, 64), (64, 64), (300, 200),
                                                 (64, 64), (64, 64), (64, 64), (300, 300), (300, 300)]

        for i in range(0, len(self.SurfacesNames)):
            self.Surfaces[self.SurfacesNames[i]] = pygame.Surface(surfaces_sizes[i])

    def draw_surfaces(self, game_window: pygame.Surface):
        positions: List[Tuple[int, int]] = [(220, 15), (50, 670), (380, 90), (600, 90), (700, 540),
                                            (110, 600),
                                            (310, 600), (520, 600), (100, 200), (600, 200)]

        for i in range(0, len(self.SurfacesNames)):
            game_window.blit(self.Surfaces[self.SurfacesNames[i]], positions[i])


@dataclass
class GUI(GameSurface):
    def __init__(self):
        super().__init__()

    def draw_background(self, sprites_ui: dict):
        background_sprite: pygame.sprite = sprites_ui['guiBackground']

        for surface_name in self.SurfacesNames:
            surface_size: Tuple[int, int] = self.__get_surface_size(self.Surfaces[surface_name])
            resized_backgroud: pygame.Surface = pygame.transform.scale(background_sprite, surface_size)
            self.Surfaces[surface_name].blit(resized_backgroud, (0, 0))

    def draw_bars(self, sprites_ui: dict):
        bar_sprites_names: List[str] = ['barBlackLeft', 'barBlackRight', 'barBlackMid']
        bar_surface_names: Tuple[str, str] = ('DishBar', 'PlayerBar')

        for surface_name in bar_surface_names:
            for sprite_name in bar_sprites_names:
                sprite: pygame.sprite = sprites_ui[sprite_name]
                self.__draw_bar_element(sprite_name, sprite, surface_name)

    def fill_bars(self, sprites_ui: dict, bar_position: int):
        player_bar_names: List[str] = ['barGreenLeft', 'barGreenRight', 'barGreenMid']
        dishes_bar_names: List[str] = ['barRedLeft', 'barRedRight', 'barRedMid']
        bar_surface_names: Tuple[str, str] = ('DishBar', 'PlayerBar')

        self.__draw_bar_filling(player_bar_names, sprites_ui, bar_surface_names[1], bar_position)
        self.__draw_bar_filling(dishes_bar_names, sprites_ui, bar_surface_names[0], bar_position)

    def add_icons(self, icons_sprites: dict):
        icons_names: List[str] = ['mug', 'pan', 'pot']
        icons_surface_names: List[str] = ['DirtyDishes', 'CleanDishes', 'PlayerActions']

        for surface_name in icons_surface_names:
            for icon_name in icons_names:
                if surface_name == 'DirtyDishes' or surface_name == 'CleanDishes':
                    self.__draw_icons(icon_name, icons_sprites, surface_name)
                else:
                    self.__draw_actions(icon_name, icons_sprites, surface_name)

    def add_actions_to_queue(self, player):
        for slot in player.ActionSlots:
            if not slot['IsActionAvailable']:
                resized_sprite: pygame.Surface = self.__resize_icon_sprite(player.ActionIcons[slot['ActionName']],
                                                                           (50, 50))
                slot['ActionSurface'].blit(resized_sprite, (10, 10))

    def clear_queue(self, player):
        for surface in player.ActionSurfaces:
            surface.blit(player.ActionBackground, (0,0))

    def remove_action_slot(self, player):
        for slot in player.ActionSlots:
            if slot['IsActionTriggered'] or slot['IsActionChanelling']:
                slot['ActionSurface'].fill(pygame.Color('BLACK'))

    def add_text(self, fontfile: str, text: str, size: int, surface: pygame.Surface, position: Tuple[int, int]):
        font: pygame.font = pygame.font.Font(fontfile, size)
        text: pygame.Surface = font.render(text, False, pygame.color.Color('WHITE'), (151, 113, 74))
        surface.blit(text, position)


    def __get_surface_size(self, ui_surface: pygame.Surface) -> Tuple[int, int]:
        surface_size: Tuple[int, int] = (ui_surface.get_size())

        return surface_size

    def __draw_bar_element(self, sprite_name: str, sprite: pygame.sprite, surface_name: str):
        if sprite_name.find('Left') > -1:
            self.Surfaces[surface_name].blit(sprite, (30, 26))
        elif sprite_name.find('Right') > -1:
            self.Surfaces[surface_name].blit(sprite, (560, 26))
        elif sprite_name.find('Mid') > -1:
            resized_sprite: pygame.Surface = pygame.transform.scale(sprite, (521, 18))
            self.Surfaces[surface_name].blit(resized_sprite, (39, 26))

    def __draw_bar_filling(self, sprite_names: List[str], sprites_ui: dict, surface_name: str, position: int):
        if position == 10:
            for sprite_name in sprite_names:
                if sprite_name.find('Left') > -1:
                    self.Surfaces[surface_name].blit(sprites_ui[sprite_name], (30, 26))
        elif position == 524:
            for sprite_name in sprite_names:
                if sprite_name.find('Right') > -1:
                    self.Surfaces[surface_name].blit(sprites_ui[sprite_name], (560, 26))
        elif 10 <= position <= 523:
            for sprite_name in sprite_names:
                if sprite_name.find('Mid') > -1:
                    resized_sprite: pygame.Surface = pygame.transform.scale(sprites_ui[sprite_name], (position, 18))
                    self.Surfaces[surface_name].blit(resized_sprite, (39, 26))

    def __draw_icons(self, sprite_name: str, icons_sprites: dict, surface_name: str):
        scale: Tuple[int, int] = (50, 50)

        if sprite_name.find('mug') > -1:
            resized_sprite: pygame.surface = self.__resize_icon_sprite(icons_sprites[sprite_name], scale)
            self.Surfaces[surface_name].blit(resized_sprite, (40, 60))
        elif sprite_name.find('pan') > -1:
            resized_sprite: pygame.surface = self.__resize_icon_sprite(icons_sprites[sprite_name], scale)
            self.Surfaces[surface_name].blit(resized_sprite, (40, 135))
        elif sprite_name.find('pot') > -1:
            resized_sprite: pygame.surface = self.__resize_icon_sprite(icons_sprites[sprite_name], scale)
            self.Surfaces[surface_name].blit(resized_sprite, (40, 220))

    def __draw_actions(self, sprite_name: str, icons_sprites: dict, surface_name: str):
        scale: Tuple[int, int] = (60, 60)

        if sprite_name.find('mug') > -1:
            resized_sprite: pygame.surface = self.__resize_icon_sprite(icons_sprites[sprite_name], scale)
            self.Surfaces[surface_name].blit(resized_sprite, (40, 60))
        elif sprite_name.find('pan') > -1:
            resized_sprite: pygame.surface = self.__resize_icon_sprite(icons_sprites[sprite_name], scale)
            self.Surfaces[surface_name].blit(resized_sprite, (220, 60))
        elif sprite_name.find('pot') > -1:
            resized_sprite: pygame.surface = self.__resize_icon_sprite(icons_sprites[sprite_name], scale)
            self.Surfaces[surface_name].blit(resized_sprite, (130, 130))

    def __resize_icon_sprite(self, icon_sprite: pygame.sprite, scale: Tuple[int, int]) -> pygame.Surface:
        resized_sprite: pygame.Surface = pygame.transform.scale(icon_sprite, scale)

        return resized_sprite