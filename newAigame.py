import pygame 
import neat
import time 
import os 
import random





win_width = 1000
win_height = 600
pygame.init()
win  = pygame.display.set_mode((win_width,win_height))
bg_surface = pygame.image.load('sprites/background.jpg').convert_alpha()
bg_surface = pygame.transform.scale(bg_surface, (1000, 600)) 
base_surface =  pygame.image.load('sprites/baase.png').convert()
base_surface = pygame.transform.scale(base_surface, (5,650))
rocket_surface1 = pygame.image.load('sprites/finalrocket_3.png').convert_alpha()
rocket_surface1 = pygame.transform.scale(rocket_surface1, (150,150))
rocket_surface2 = pygame.image.load('sprites/finalrocket_2.png').convert_alpha()
rocket_surface2 = pygame.transform.scale(rocket_surface2, (150,150))
rocket_surface3 = pygame.image.load('sprites/finalrocket_1.png').convert_alpha()
rocket_surface3 = pygame.transform.scale(rocket_surface3, (150,150))
rocket_IMGs = [rocket_surface1,rocket_surface2,rocket_surface3]




    def move(self):
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d>=16:
            d = 16
        if d< 0:
            d -=2
        self.x = self.x +d

        if d < 0 or self.x < self.width +50:
            if self.tilt < self.max_rotation:
                self.tilt =self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= self.rot_vel
    
    def draw(self , win):
        counter = 1
        anim_time = 5
        counter += 1
        if counter < anim_time:
            self.img = self.IMGS[0]
        elif counter < anim_time*2:
            self.img = self.IMGS[1]
        elif counter < anim_time*3:
            self.img = self.IMGS[2]
        elif counter < anim_time*4:
            self.img = self.IMGS[1]
        elif counter < anim_time*4 + 1:
            self.img = self.IMGS[0]
            counter = 0
        
        if self.tilt <= -80:
            self.img =self.IMGS[0]
            counter = self.anim_time*2
        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image , new_rect.topleft)
        
        '''new_roc = pygame.transform.rotozoom(self.img ,self.tilt, 1)#1 is scaling factor
        roc_rect = new_roc.get_rect(center = (self.x , self.y))
        win.blit(new_roc,roc_rect)'''

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
def draw_window(win, roc):
        win.blit(bg_surface ,(0,0))
        rocket.draw(win,roc)
        pygame.display.update()




def main():

    while True:
        Rocket = rocket(500,520)
        #win  = pygame.display.set_mode((win_width,win_height))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            draw_window(win,rocket)
        pygame.quit()
        quit()
            #rocket.move()
main()
        