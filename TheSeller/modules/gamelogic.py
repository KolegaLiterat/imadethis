import pygame
from typing import List

class Actions():
    def start_production(self, workers) -> bool:
        is_worker_avaible: bool = False

        for worker in workers:
            if worker.isIdle == True:
                worker.isIdle = False
                is_worker_avaible = True
                break

        return is_worker_avaible
    
    def free_workers(self, workers):
        for worker in workers:
            if worker.isIdle == False:
                worker.isIdle = True
    
    def calculate_growth_for_resource(self, supply, value_change):
        supply.growth = supply.growth + value_change
    
    def calculate_usage_of_resources(self, resources, value_change):
        for resource in resources:
            resource.selling = resource.selling - value_change

    def check_is_supply_producable(self, supply, resources, value_change) -> bool:
        is_supply_producable: bool = False
        
        if len(resources) == 1:
            if self.__check_one_additonal_resources(supply, resources, value_change):
                is_supply_producable = True
        else:
            if self.__check_two_additional_resources(resources, value_change):
                is_supply_producable = True

        return is_supply_producable

    def check_is_supply_sellable(self, supply, value_change) -> bool:
        is_supply_sellable = False

        if supply.amount - supply.selling + value_change >= 0:
            is_supply_sellable = True

        return is_supply_sellable

    def sell_supplies(self, supply, value_change) -> bool:
        supply.selling = supply.selling - value_change
    
    def change_supplies_amount(self, supplies):
        for supply in supplies:
            if supply.growth != 0:
                supply.amount = supply.amount + supply.growth
                supply.growth = 0
            if supply.selling != 0:
                supply.amount = supply.amount - supply.selling
                supply.selling = 0

    def __check_one_additonal_resources(self, supply, resources, value_change) -> bool:
        is_there_enough_supplies: bool = False

        if resources[0].amount - resources[0].selling + value_change >= 0:
            is_there_enough_supplies = True

        return is_there_enough_supplies
    
    def __check_two_additional_resources(self, resources, value_change) -> bool:
        is_there_enough_supplies: bool = False

        if resources[0].amount - resources[0].selling + value_change >= 0:
            if resources[1].amount - resources[1].selling + value_change >0:
                is_there_enough_supplies = True

        return is_there_enough_supplies