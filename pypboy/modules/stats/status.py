from game.core import Entity

# Position adjustments
x_adjust = 30
y_adjust = -55
scale_adj = 0.75

import pypboy
import pygame
import game
import settings
import pypboy.ui
import os
import time
global STATION

class Module(pypboy.SubModule):
    global STATION
    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        
        self.label = "STATUS"
        self.images = []

        self.topmenu = pypboy.ui.TopMenu()
        self.add(self.topmenu)
        self.topmenu.label = "STAT"
        self.topmenu.title = settings.MODULE_TEXT


        self.health = Health()
        self.health.rect[0] = 0 + x_adjust
        self.health.rect[1] = 131 + y_adjust
        self.add(self.health)

        self.animation = Animation()
        self.animation.rect[0] = 296 + x_adjust
        self.animation.rect[1] = 190 + y_adjust
        self.add(self.animation)

        self.prev_time = 0

        self.footer = pypboy.ui.Footer(settings.STATUS_FOOTER)
        self.footer.rect[0] = settings.footer_x
        self.footer.rect[1] = settings.footer_y
        self.add(self.footer)
        # STATUS_FOOTER = ["HP 115/115", "LEVEL 66", "AP 90/90", 90, True]

    #     self.menu = pypboy.ui.Menu(["CND", "RAD", "EFF"], [self.show_cnd, self.show_rad, self.show_eff], 0)
    #     self.menu.rect[0] = settings.menu_x
    #     self.menu.rect[1] = settings.menu_y
    #     self.add(self.menu)

    # def show_cnd(self):
    #     print("CND")

    # def show_rad(self):
    #     print("RAD")

    # def show_eff(self):
    #     print("EFF")

    def render(self, *args, **kwargs):
        global STATION
        if settings.glitch == True:
            self.current_time = time.time()
            self.delta_time = self.current_time - self.prev_time

            if self.delta_time >= settings.glitch_time:
                if settings.glitch_next == 0 or settings.glitch_next == 2 or settings.glitch_next == 4:
                    self.health.rect[1] = -69 + y_adjust
                    self.footer.rect[1] = 62 + y_adjust
                    self.animation.rect[1] = -10 + y_adjust
                    self.prev_time = self.current_time
                elif settings.glitch_next == 1 or settings.glitch_next == 3 or settings.glitch_next == 5:
                    self.health.rect[1] = 331 + y_adjust
                    self.footer.rect[1] = 531 + y_adjust
                    self.animation.rect[1] = 390 + y_adjust
                    self.prev_time = self.current_time
                elif settings.glitch_next == 6:
                    self.health.rect[1] = 131 + y_adjust
                    self.animation.rect[1] = 190 + y_adjust
                    self.footer.rect[1] = settings.footer_y + y_adjust
                    self.prev_time = self.current_time
                elif settings.glitch_next >= 7:
                    settings.glitch_next = 0
                    settings.glitch = False
                settings.glitch_next += 1

    # def handle_resume(self):
    #     pass
    #     super(Module, self).handle_resume()

class Animation(game.Entity):

    def __init__(self):
        super(Animation, self).__init__()

        self.image = pygame.Surface((settings.WIDTH - 50, settings.HEIGHT))
        self.animation_time = 0.125 # 8 fps
        self.steps = list(range(4)) + list(range(4, 0, -1))
        self.index = 0                
        self.images = []
        self.prev_time = 0
        self.prev_fps_time = 0

        path = "./images/stats/legs1"
        for f in  sorted(os.listdir(path)):
            if f.endswith(".png"):
                image = pygame.image.load(path + "/" + f).convert_alpha()
                self.images.append(image)
        self.head = pygame.image.load("images/stats/head1/1.png").convert_alpha()

    def render(self, *args, **kwargs):

        self.current_time = time.time()
        self.delta_time = self.current_time - self.prev_time

        # #FPS debugging
        # self.fps_delta_time = self.current_time - self.prev_fps_time
        # if self.fps_delta_time:
        #     self.fps = round(1/self.fps_delta_time,1)
        # self.prev_fps_time = time.time()

        if self.delta_time >= self.animation_time:
            self.prev_time = self.current_time

            self.image.fill((0,0,0))

            if self.index >= len(self.images):
                self.index = 0
            self.file = self.images[self.index]
            
            scaled_file = pygame.transform.smoothscale(self.file, (self.file.get_width() * scale_adj, self.file.get_height() * scale_adj))
            scaled_head = pygame.transform.smoothscale(self.head, (self.head.get_width() * scale_adj, self.head.get_height() * scale_adj))
    
            self.image.blit((scaled_file), (20 + self.steps[self.index] // 2 + x_adjust * scale_adj, 20 + 78 + self.steps[self.index] + y_adjust * scale_adj))
            self.image.blit((scaled_head), (41 + self.steps[self.index] // 2 + x_adjust * scale_adj, 20 + 25 + self.steps[self.index] + y_adjust * scale_adj))
            # settings.FreeRobotoB[24].render_to(self.image, (0, 0), str(self.fps), settings.bright) #FPS

            self.index += 1


class Health(game.Entity):

    def __init__(self):
        super(Health, self).__init__()

        self.image = pygame.Surface((settings.WIDTH - 50, settings.HEIGHT - 80))
        self.image.fill((0,0,0))

        # Middle Boxes
        pygame.draw.rect(self.image, settings.dim, (203 + x_adjust, 358 + y_adjust, 64, 62)) #Gun box
        pygame.draw.rect(self.image, settings.dim, (273 + x_adjust, 358 + y_adjust, 38, 62)) #Ammo box
        pygame.draw.rect(self.image, settings.dim, (328 + x_adjust, 358 + y_adjust, 64, 62)) #Helmet box
        pygame.draw.rect(self.image, settings.dim, (398 + x_adjust, 358 + y_adjust, 38, 62)) #Armor box
        pygame.draw.rect(self.image, settings.dim, (440 + x_adjust, 358 + y_adjust, 38, 62)) #Energy box
        pygame.draw.rect(self.image, settings.dim, (483 + x_adjust, 358 + y_adjust, 38, 62)) #Radiation box

        # Icons
        self.image.blit(pygame.image.load('images/stats/gun.png').convert_alpha(),(210 + x_adjust,374 + y_adjust))
        self.image.blit(pygame.image.load('images/stats/reticle.png').convert_alpha(),(284 + x_adjust,363 + y_adjust))
        self.image.blit(pygame.image.load('images/stats/helmet.png').convert_alpha(),(338 + x_adjust,373 + y_adjust))
        self.image.blit(pygame.image.load('images/stats/shield.png').convert_alpha(),(410 + x_adjust,362 + y_adjust))
        self.image.blit(pygame.image.load('images/stats/bolt.png').convert_alpha(),(453 + x_adjust,362 + y_adjust))
        self.image.blit(pygame.image.load('images/stats/radiation.png').convert_alpha(),(491 + x_adjust,363 + y_adjust))

        # Health Bars
        pygame.draw.line(self.image, settings.bright, (344 + x_adjust, 45 + 32 + y_adjust), (379 + x_adjust, 45 + 32 + y_adjust), 9)
        pygame.draw.line(self.image, settings.bright, (465 + x_adjust, 134 + y_adjust), (500 + x_adjust, 134 + y_adjust), 9)
        pygame.draw.line(self.image, settings.bright, (465 + x_adjust, 266 + y_adjust), (500 + x_adjust, 266 + y_adjust), 9)
        pygame.draw.line(self.image, settings.bright, (344 + x_adjust, 318 + y_adjust), (379 + x_adjust, 318 + y_adjust), 9)
        pygame.draw.line(self.image, settings.bright, (216 + x_adjust, 266 + y_adjust), (251 + x_adjust, 266 + y_adjust), 9)
        pygame.draw.line(self.image, settings.bright, (216 + x_adjust, 134 + y_adjust), (251 + x_adjust, 134 + y_adjust), 9)

        #Stat text
        settings.FreeRobotoB[24].render_to(self.image, (281 + x_adjust, 395 + y_adjust), "18", settings.bright) # Ammo count
        settings.FreeRobotoB[24].render_to(self.image, (406 + x_adjust, 395 + y_adjust), "10", settings.bright) # Armor count
        settings.FreeRobotoB[24].render_to(self.image, (447 + x_adjust, 395 + y_adjust), "20", settings.bright) # Energy count
        settings.FreeRobotoB[24].render_to(self.image, (490 + x_adjust, 395 + y_adjust), "10", settings.bright) # Rad count

        #User name
        settings.FreeRobotoB[24].render_to(self.image, (301 + x_adjust, 448 + y_adjust), settings.name, settings.bright)

    # def handle_resume(self):
    #     pass
    #     super(Module, self).handle_resume()
