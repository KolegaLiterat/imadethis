import pygame
import windowManager
import assetManager
import gameEvents
from typing import Tuple, List
from dataclasses import dataclass


@dataclass
class GameManager:
    def __init__(self):
        self.IsGameRunning: bool = True
        self.IsPlayerFailed: bool = False
        self.MainWindow = windowManager.GameWindow((1024, 768)).create_window()
        self.SurfaceManagerGUI = windowManager.GUI()
        self.AssetsGUI = assetManager.UI()
        self.FPS = pygame.time.Clock()

    def run_game(self):
        pygame.init()

        self.__create_gui()
        self.__create_text()

        enemy = gameEvents.DishEvents([self.SurfaceManagerGUI.Surfaces['Dish0'],
                                       self.SurfaceManagerGUI.Surfaces['Dish1']],
                                      self.AssetsGUI.UISprites['guiBackground'],
                                      self.AssetsGUI.Icons)

        player = gameEvents.PlayerEvents([self.SurfaceManagerGUI.Surfaces['PlayerAction0'],
                                          self.SurfaceManagerGUI.Surfaces['PlayerAction1'],
                                          self.SurfaceManagerGUI.Surfaces['PlayerAction2']],
                                         self.AssetsGUI.UISprites['guiBackground'],
                                         self.AssetsGUI.Icons)

        bar_position: int = 10

        while self.IsGameRunning:
            if enemy.EmptySlots > 0:
                if bar_position == 10:
                    enemy.create_dishes()
                    player.ActionSlots.clear()
                    player.create_action_slots()
                    self.SurfaceManagerGUI.clear_queue(player)
                    self.SurfaceManagerGUI.draw_bars(self.AssetsGUI.UISprites)

                self.FPS.tick(30)
                self.SurfaceManagerGUI.draw_surfaces(self.MainWindow)
                self.SurfaceManagerGUI.fill_bars(self.AssetsGUI.UISprites, bar_position)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.IsGameRunning = False
                    elif event.type == pygame.MOUSEBUTTONUP:
                        position = pygame.mouse.get_pos()
                        player.add_action_to_queue(position)
                        self.SurfaceManagerGUI.add_actions_to_queue(player)

                enemy.update_dirty_dishes(bar_position)
                player.trigger_action(bar_position)
                enemy.update_empty_slots()
                player.update_clean_dishes(enemy)
                self.__update_statuses(enemy, player)
                self.SurfaceManagerGUI.remove_action_slot(player)

                pygame.display.update()
                bar_position = self.__change_position(bar_position)

            elif enemy.EmptySlots == 0:
                self.MainWindow.fill(pygame.Color('BLACK'))
                score = player.DishAmount['mug'] + player.DishAmount['pot'] + player.DishAmount['pan']
                text: str = 'Your score is ' + str(score)
                self.SurfaceManagerGUI.add_text(self.AssetsGUI.Fonts['Kenney Bold'], text, 30, self.MainWindow,
                                                (400, 400))
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.IsGameRunning = False
    pygame.quit()

    def __update_statuses(self, enemy, player):
        self.__update_dishes(enemy, player)
        self.__update_slots(enemy)

    def __create_gui(self):
        self.SurfaceManagerGUI.create_surface()
        self.AssetsGUI.load_sprites()
        self.AssetsGUI.load_fonts()
        self.AssetsGUI.load_icons()
        self.SurfaceManagerGUI.draw_background(self.AssetsGUI.UISprites)
        self.SurfaceManagerGUI.add_icons(self.AssetsGUI.Icons)

    def __create_text(self):
        self.SurfaceManagerGUI.add_text(self.AssetsGUI.Fonts['Kenney Bold'], 'Dish Bar', 13,
                                        self.SurfaceManagerGUI.Surfaces['DishBar'], (60, 5))
        self.SurfaceManagerGUI.add_text(self.AssetsGUI.Fonts['Kenney Bold'], 'Player Bar', 13,
                                        self.SurfaceManagerGUI.Surfaces['PlayerBar'], (60, 5))
        self.SurfaceManagerGUI.add_text(self.AssetsGUI.Fonts['Kenney Bold'], 'Slots left', 15,
                                        self.SurfaceManagerGUI.Surfaces['DirtyDishes'], (40, 20))
        self.SurfaceManagerGUI.add_text(self.AssetsGUI.Fonts['Kenney Bold'], 'Items clean', 15,
                                        self.SurfaceManagerGUI.Surfaces['CleanDishes'], (80, 20))
        self.SurfaceManagerGUI.add_text(self.AssetsGUI.Fonts['Kenney Bold'], 'Actions', 15,
                                        self.SurfaceManagerGUI.Surfaces['PlayerActions'], (100, 20))

    def __change_position(self, bar_position: int) -> int:
        if 10 <= bar_position <= 523:
            bar_position = bar_position + 2
        else:
            bar_position = 10

        return bar_position

    def __update_slots(self, enemy):
        surface: pygame.surface = self.SurfaceManagerGUI.Surfaces['DirtyDishes']
        self.SurfaceManagerGUI.add_text(self.AssetsGUI.Fonts['Kenney Bold'], str(enemy.EmptySlots), 15,
                                        surface, (200, 20))

    def __update_dishes(self, enemy, player):
        surface_names: Tuple[str, str] = ('DirtyDishes', 'CleanDishes')

        y: int = 80

        for surface_name in surface_names:
            if surface_name == 'DirtyDishes':
                self.__dirty_dishes(y, enemy, surface_name)
            else:
                self.__dirty_dishes(y, player, surface_name)
            y = 80

    def __dirty_dishes(self, y: int, enemy, surface_name: str):
        dish_types: List[str] = enemy.DishAmount.keys()

        for dish_type in dish_types:
            text = 'x        ' + str(enemy.DishAmount[dish_type])

            self.SurfaceManagerGUI.add_text(self.AssetsGUI.Fonts['Kenney Bold'], text, 25,
                                            self.SurfaceManagerGUI.Surfaces[surface_name], (140, y))
            y = y + 80
