#libs
import pygame
import datetime

#modules
from modules.gui import UserInterface
from modules.sprites import Sprites
from modules.supplies import Supplies
from modules.workers import Workers
from modules.demand import Demand
from modules.gamelogic import Actions

pygame.init()
window = pygame.display.set_mode((1280, 720))
worker_and_supplies_font = pygame.font.Font('./font/kennyFont.ttf', 70)
demand_font = pygame.font.Font('./font/kennyFont.ttf', 35)
information_font = pygame.font.Font('./font/kennyFont.ttf', 30)
pygame.display.set_caption('The Seller')

actions = Actions()

gui = UserInterface()
gui.create_lines_for_gui(window)

sprites_for_tokens = Sprites()
sprites_for_tokens.load_sprites()

workers_objects = pygame.sprite.Group()
resource_objects = pygame.sprite.Group()
demand_objects = pygame.sprite.Group()

RESOURCE_BUCKET_ORE     = Supplies((400, 140), sprites_for_tokens.loaded_sprites[0], 'bucket of ore', False, 0, 0, 0)
RESOURCE_BUCKET_WATER   = Supplies((400, 250), sprites_for_tokens.loaded_sprites[1], 'bucket of water', True, 0, 0, 0)
RESOURCE_CLAM_CLOSED    = Supplies((400, 360), sprites_for_tokens.loaded_sprites[2], 'clam', False, 0, 0, 0)
RESOURCE_CLAM_OPEN      = Supplies((400, 470), sprites_for_tokens.loaded_sprites[3], 'opened clam', True, 0, 0, 0)
RESOURCE_MEAT_COOKED    = Supplies((400, 580), sprites_for_tokens.loaded_sprites[4], 'cooked meat', True, 0, 0, 0)
RESOURCE_MEAT_RAW       = Supplies((650, 140), sprites_for_tokens.loaded_sprites[5], 'raw meat', False, 0, 0, 0)
RESOURCE_TOOL_SHOVEL    = Supplies((650, 250), sprites_for_tokens.loaded_sprites[6], 'shovel', True, 0, 0, 0)
RESOURCE_TOOL_SWORD     = Supplies((650, 360), sprites_for_tokens.loaded_sprites[7], 'sword', True, 0, 0, 0)
RESOURCE_WOOD_LOG       = Supplies((650, 470), sprites_for_tokens.loaded_sprites[8], 'log', False, 0, 0, 0)
RESOURCE_WOOD_TREE      = Supplies((650, 580), sprites_for_tokens.loaded_sprites[9], 'tree', False, 0, 0, 0)
DEMAND_BUCKET_WATER     = Demand((1050, 100), sprites_for_tokens.loaded_sprites[1], 'bucket of water', 0, 0)
DEMAND_CLAM_OPEN        = Demand((1050, 230), sprites_for_tokens.loaded_sprites[3], 'opened clam', 0, 0)
DEMAND_MEAT_COOKED      = Demand((1050, 360), sprites_for_tokens.loaded_sprites[4], 'cooked meat', 0, 0)
DEMAND_TOOL_SHOVEL      = Demand((1050, 490), sprites_for_tokens.loaded_sprites[6], 'shovel',0, 0)
DEMAND_TOOL_SWORD       = Demand((1050, 620), sprites_for_tokens.loaded_sprites[7], 'sword', 0, 0)
WORKER1                 = Workers((80, 130), sprites_for_tokens.loaded_sprites[10], True)
WORKER2                 = Workers((80, 220), sprites_for_tokens.loaded_sprites[10], True)
WORKER3                 = Workers((80, 310), sprites_for_tokens.loaded_sprites[10], True)
WORKER4                 = Workers((80, 400), sprites_for_tokens.loaded_sprites[10], True)
WORKER5                 = Workers((80, 490), sprites_for_tokens.loaded_sprites[10], True)
WORKER6                 = Workers((80, 580), sprites_for_tokens.loaded_sprites[10], True)

resource_objects.add(RESOURCE_BUCKET_ORE, RESOURCE_BUCKET_WATER, RESOURCE_CLAM_CLOSED,
                     RESOURCE_CLAM_OPEN, RESOURCE_MEAT_COOKED, RESOURCE_MEAT_RAW,
                     RESOURCE_TOOL_SHOVEL, RESOURCE_TOOL_SWORD, RESOURCE_WOOD_LOG,
                     RESOURCE_WOOD_TREE)
resource_objects.update()
resource_objects.draw(window)

demand_objects.add(DEMAND_BUCKET_WATER, DEMAND_CLAM_OPEN,
                   DEMAND_MEAT_COOKED, DEMAND_TOOL_SHOVEL, DEMAND_TOOL_SWORD)
demand_objects.update()
demand_objects.draw(window)

workers_objects.add(WORKER1, WORKER2, WORKER3, WORKER4, WORKER5, WORKER6)
workers_objects.update()
workers_objects.draw(window)

fps = pygame.time.Clock()
is_game_running: bool = True
happines = 100
end_turn = True
action_menu = False
selected_supply = None

def produce_supplies_with_one_resource(selected_supply, resources, value_change):
    if actions.check_is_supply_producable(selected_supply, resources, -1):
        if actions.start_production(workers_objects):
            actions.calculate_growth_for_resource(selected_supply, value_change)
            actions.calculate_usage_of_resources(resources, -1)
        else:
            gui.action_informations(window, information_font, 'noFreeWorkers')
    else:
        gui.action_informations(window, information_font, 'notEnoughResources')

def produce_supplies(value_change: int):
    resources = []

    if selected_supply.name == 'opened clam':
        resources.append(RESOURCE_CLAM_CLOSED)
        produce_supplies_with_one_resource(selected_supply, resources, value_change)
        resources.clear()
    elif selected_supply.name == 'cooked meat':
        resources.append(RESOURCE_MEAT_RAW)
        produce_supplies_with_one_resource(selected_supply, resources, value_change)
        resources.clear()
    elif selected_supply.name == 'shovel':
        resources.extend((RESOURCE_WOOD_LOG, RESOURCE_BUCKET_ORE))
        produce_supplies_with_one_resource(selected_supply, resources, value_change)
        resources.clear()
    elif selected_supply.name == 'sword':
        pass
    elif selected_supply.name == 'log':
        resources.append(RESOURCE_WOOD_TREE)
        produce_supplies_with_one_resource(selected_supply, resources, value_change)
        resources.clear()
    else:
        if actions.start_production(workers_objects):
            actions.calculate_growth_for_resource(selected_supply, value_change)
        else:
            gui.action_informations(window, information_font, 'noFreeWorkers')

    # if actions.check_is_supply_producable(selected_supply, resource_objects, value_change):
    #     if actions.start_production(workers_objects):
    #         actions.calculate_growth_for_resource(selected_supply, value_change)
    #     else:
    #         gui.action_informations(window, information_font, 'noFreeWorkers')
    # else:
    #     gui.action_informations(window, information_font, 'notEnoughResources')

def supplies_selling(value_change: int):
    if actions.check_is_supply_sellable(selected_supply, value_change):
        if actions.start_production(workers_objects):
            actions.sell_supplies(selected_supply, value_change)
        else:
            gui.action_informations(window, information_font, 'noFreeWorkers')
    else:
        gui.action_informations(window, information_font, 'negativeAmount')


while is_game_running:
    fps.tick(30)
    
    gui.create_text_with_workers_status(worker_and_supplies_font, window, workers_objects)
    gui.create_text_with_supplies_amounts(worker_and_supplies_font, window, resource_objects)
    gui.create_text_with_demand_information(demand_font, window, demand_objects)
    gui.create_text_with_happines(window, demand_font, happines)
    
    if happines > 0:
        if end_turn == True:
            actions.free_workers(workers_objects)
            actions.change_supplies_amount(resource_objects)
            end_turn = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()

                for supply in resource_objects:
                    if supply.rect.collidepoint(mouse_position):
                        gui.on_click_actions(window, information_font, supply, demand_objects)
                        action_menu = True
                        selected_supply = supply

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    pygame.image.save(window, 'screen.png')
                if event.key == pygame.K_f:
                    end_turn = True
                    action_menu = False
                    gui.action_informations(window, information_font, 'endTurn')
                if event.key == pygame.K_p and action_menu:
                    produce_supplies(1)                
                if event.key == pygame.K_s and action_menu:
                    supplies_selling(-1)
                if event.key == pygame.K_d and action_menu:
                    supplies_selling(-5)

    pygame.display.update()
    
pygame.quit()
