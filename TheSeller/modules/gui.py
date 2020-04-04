import pygame

class UserInterface:

    def create_lines_for_gui(self, window_to_draw):
        pygame.draw.line(window_to_draw, pygame.Color('White'), pygame.Vector2(
            362, 40), pygame.Vector2(362, 680), 10)
        
        pygame.draw.line(window_to_draw, pygame.Color('White'), pygame.Vector2(
            900, 40), pygame.Vector2(900, 680), 10)
    
    def create_text_with_workers_status(self, font, window_to_draw, workers):
        for worker in workers:
            if worker.isIdle == True:
                window_to_draw.fill(pygame.Color('Black'), (worker.position[0] + 40, worker.position[1] - 30, 150, 64))
                idleText = font.render('Idle!', 0, pygame.color.Color('White'))
                window_to_draw.blit(idleText, (worker.position[0] + 40, worker.position[1] - 30))
            else:
                window_to_draw.fill(pygame.Color('Black'), (worker.position[0] + 40, worker.position[1] - 30, 150, 64))
                workingText = font.render('Busy!', 0, pygame.color.Color('White'))
                window_to_draw.blit(workingText, (worker.position[0] + 40, worker.position[1] - 30))
    
    def create_text_with_supplies_amounts(self, font, window_to_draw, supplies):
        for supply in supplies:
            window_to_draw.fill(pygame.Color('Black'), (supply.position[0] + 40, supply.position[1] - 30, 185, 64))
            amount_text = font.render('  ' + str(supply.amount) + '  ' + str(supply.growth) + '  ' + str(supply.selling), 0, (255, 255, 255))
            window_to_draw.blit(amount_text, (supply.position[0] + 40, supply.position[1] - 30))

    def create_text_with_demand_information(self, font, window_to_draw, demands):
        for demand in demands:
            window_to_draw.fill(pygame.Color('Black'), (demand.position[0] - 100, demand.position[1] + 25, 350, 64))
            demand_amount = font.render('Demand: ' + str(int(demand.amount)), 0, pygame.color.Color('White'))
            window_to_draw.blit(demand_amount, (demand.position[0] - 30, demand.position[1] + 25))
            demand_growth = font.render('Growth per turn: ' + str(int(demand.growth)), 0, pygame.color.Color('White'))
            window_to_draw.blit(demand_growth, (demand.position[0] - 80, demand.position[1] + 50))
    
    def create_text_with_happines(self, window_to_draw, font, value):
        window_to_draw.fill(pygame.Color('Black'), (1000, 10, 200, 35))
        happines_value = font.render('Happines: ' + str(value), 0, pygame.color.Color('White'))
        window_to_draw.blit(happines_value, (1000, 10))

    def on_click_actions(self, window_to_draw, font, supply_object, demand_objects):
        window_to_draw.fill(pygame.color.Color('Black'), (400, 620, 430, 100))
        
        for demand in demand_objects:
            if supply_object.name == demand.name:
                self.__create_sell_and_produce_text(window_to_draw, font, supply_object)
            else:
                self.__create_only_produce_text(window_to_draw, font, supply_object)

    def action_informations(self, window_to_draw, font, information_type):
        if information_type == 'noFreeWorkers':
            message = font.render('No more free workers! Press F to end turn!', 0, pygame.color.Color('RED'))
        elif information_type == 'negativeAmount':
            message = font.render('Not enough supplies for sell!', 0, pygame.color.Color('Red'))
        elif information_type == 'endTurn':
            message = font.render('Turn ended!', 0, pygame.color.Color('White'))
        elif information_type == 'notEnoughResources':
            message = font.render('Not enough resources to produce supply!', 0, pygame.color.Color('Red'))

        window_to_draw.fill(pygame.color.Color('Black'), (400, 620, 430, 100))
        window_to_draw.blit(message, (400, 620))
    
    def __create_sell_and_produce_text(self, window_to_draw, font, supply_object):
        produce_text = font.render('To produce 1 ' + supply_object.name + ' press P', 0, pygame.color.Color('White'))
        sell_one_text = font.render('To sell 1 ' + supply_object.name + ' press S', 0, pygame.color.Color('White'))
        sell_five_text = font.render('To sell 5 ' + supply_object.name + ' press D', 0, pygame.color.Color('White'))
        window_to_draw.blit(produce_text, (400, 620))
        window_to_draw.blit(sell_one_text, (400, 655))
        window_to_draw.blit(sell_five_text, (400, 690))
    
    def __create_only_produce_text(self, window_to_draw, font, supply_object):
        produce_text = font.render('To produce 1 ' + supply_object.name + ' press P', 0, pygame.color.Color('White'))
        window_to_draw.blit(produce_text, (400, 620))