import pygame
import random
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class DishEvents:
    def __init__(self, dish_surfaces: list, background: pygame.sprite, icons: dict):
        self.DishSurfaces = dish_surfaces
        self.DishBackgroud = background
        self.Icons = icons
        self.EmptySlots = 3
        self.ActiveDishes = []
        self.DishAmount = {'mug': 0,
                           'pan': 0,
                           'pot': 0, }
        self.EventTriggerPositon: Tuple[int, int] = (170, 380)

    def create_dishes(self):

        tuple_index: int = 0

        for surface in self.DishSurfaces:
            dish_type = self.__choose_type()
            self.__update_surface(surface, dish_type)

            new_dish: List[str, int] = [dish_type, self.EventTriggerPositon[tuple_index]]
            self.ActiveDishes.append(new_dish)

            tuple_index = tuple_index + 1

    def update_dirty_dishes(self, bar_postion: int):
        for dish in self.ActiveDishes:
            if bar_postion == dish[1]:
                amount: int = self.DishAmount[dish[0]] + 1
                self.DishAmount[dish[0]] = amount
                self.ActiveDishes.pop(0)

                self.update_empty_slots()

    def __choose_type(self) -> str:
        dish_types: List[str] = ['mug', 'pot', 'pan']
        dish_type = random.choice(dish_types)

        return dish_type

    def __update_surface(self, surface: pygame.Surface, dish_type: str):
        resized_background: pygame.Surface = pygame.transform.scale(self.DishBackgroud, surface.get_size())
        surface.blit(resized_background, (0, 0))
        resized_sprite = pygame.transform.scale(self.Icons[dish_type], (45, 45))
        surface.blit(resized_sprite, (10, 10))

    def update_empty_slots(self):
        dishes_sum = 0

        for dish in self.DishAmount.items():
            dishes_sum: int = dishes_sum + dish[1]

        self.EmptySlots = 3 - dishes_sum


@dataclass
class PlayerEvents:
    def __init__(self, action_surfaces: list, action_background: pygame.sprite, icons):
        self.ActionSurfaces = action_surfaces
        self.ActionBackground = action_background
        self.ActionIcons = icons
        self.ActionSlots = []
        self.AcionTriggers: Tuple[int, int, int] = (60, 250, 460)
        self.DishAmount = {'mug': 0,
                            'pan': 0,
                            'pot': 0,}

    def create_action_slots(self):
        for surface in self.ActionSurfaces:
            action_slot = {
                'ActionSurface': surface,
                'ActionName': None,
                'IsActionAvailable': True,
                'IsActionTriggered': False,
                'IsActionChanelling': False,
                'IsDishCounted': False,
            }

            self.ActionSlots.append(action_slot)

    def add_action_to_queue(self, mouse_position: Tuple[int, int]):
        free_slots: int = self.__get_free_slots()
        action_name = self.__return_action(mouse_position)

        if action_name != 'None':
            if action_name == 'mug' or action_name=='pot' and free_slots < 4:
                self.__create_action_for_mug(free_slots, action_name)
            elif action_name == 'pan' and free_slots > 1:
                self.__create_action_for_pan(free_slots, action_name)
            else:
                print('Note enoug action slots!')

    def trigger_action(self, bar_position):
        if bar_position == self.AcionTriggers[0]:
            if self.ActionSlots[0]['IsActionChanelling'] == False:
                self.ActionSlots[0]['IsActionTriggered'] = True
        elif bar_position == self.AcionTriggers[1]:
            if self.ActionSlots[1]['IsActionChanelling'] == False:
                self.ActionSlots[1]['IsActionTriggered'] = True
        elif bar_position == self.AcionTriggers[2]:
            if self.ActionSlots[2]['IsActionChanelling'] == False:
                self.ActionSlots[2]['IsActionTriggered'] = True

    def update_clean_dishes(self, enemy):
        for slot in self.ActionSlots:
            if slot['IsActionTriggered'] == True and slot['IsDishCounted'] == False:
                if slot['ActionName'] != None:
                    new_dish_amount = enemy.DishAmount[slot['ActionName']] - 1

                    if new_dish_amount > -1:
                        enemy.DishAmount[slot['ActionName']] = enemy.DishAmount[slot['ActionName']] - 1
                        self.DishAmount[slot['ActionName']] = self.DishAmount[slot['ActionName']] + 1
                        slot['IsDishCounted'] = True

    def __get_free_slots(self) -> int:
        free_slots: int = 0

        for slot in self.ActionSlots:
            if slot['IsActionAvailable'] and slot['IsActionTriggered'] == False:
                free_slots = free_slots + 1

        return free_slots

    def __return_action(self, mouse_position: Tuple[int, int]):
        action: str = 'NONE'

        if 741 <= mouse_position[0] <= 785 and 605 <= mouse_position[1] <= 656:
            action = 'mug'
        elif 925 <= mouse_position[0] <= 971 and 601 <= mouse_position[1] <= 654:
            action = 'pan'
        elif 834 <= mouse_position[0] <= 888 and 670 <= mouse_position[1] <= 726:
            action = 'pot'

        return action

    def __create_action_for_mug(self, free_slots, action_name):
        if free_slots == 3:
            if self.ActionSlots[0]['IsActionTriggered'] == False:
                self.ActionSlots[0]['ActionName'] = action_name
                self.ActionSlots[0]['IsActionAvailable'] = False
        elif free_slots == 2:
            if self.ActionSlots[1]['IsActionTriggered'] == False:
                self.ActionSlots[1]['ActionName'] = action_name
                self.ActionSlots[1]['IsActionAvailable'] = False
        elif free_slots == 1:
            if self.ActionSlots[2]['IsActionTriggered'] == False:
                self.ActionSlots[2]['ActionName'] = action_name
                self.ActionSlots[2]['IsActionAvailable'] = False

    def __create_action_for_pan(self, free_slots, action_name):
        if free_slots == 3:
            if not self.ActionSlots[0]['IsActionTriggered']:
                self.ActionSlots[0]['ActionName'] = action_name
                self.ActionSlots[0]['IsActionAvailable'] = False
                self.ActionSlots[1]['ActionName'] = action_name
                self.ActionSlots[1]['IsActionAvailable'] = False
                self.ActionSlots[1]['IsActionChanelling'] = True
        elif free_slots == 2:
            if not self.ActionSlots[1]['IsActionTriggered']:
                self.ActionSlots[1]['ActionName'] = action_name
                self.ActionSlots[1]['IsActionAvailable'] = False
                self.ActionSlots[2]['ActionName'] = action_name
                self.ActionSlots[2]['IsActionAvailable'] = False
                self.ActionSlots[2]['IsActionChanelling'] = True
