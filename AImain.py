import pygame 
import neat
import time 
import os 
import random

pygame.font.init()
win_width = 1000
win_height = 600
STAT_FONT = pygame.font.SysFont("comicsans", 50)
pygame.init()
win  = pygame.display.set_mode((win_width,win_height))
clock = pygame.time.Clock()
bg_surface = pygame.image.load('sprites/background.jpg').convert_alpha()
bg_surface = pygame.transform.scale(bg_surface, (1000, 600)) 
base_surface =  pygame.image.load('sprites/baase.png').convert()
base_surface = pygame.transform.scale(base_surface, (5,690))
rocket_surface1 = pygame.image.load('sprites/finalrocket_3.png').convert_alpha()
rocket_surface1 = pygame.transform.scale(rocket_surface1, (150,150))
rocket_surface2 = pygame.image.load('sprites/finalrocket_2.png').convert_alpha()
rocket_surface2 = pygame.transform.scale(rocket_surface2, (150,150))
rocket_surface3 = pygame.image.load('sprites/finalrocket_1.png').convert_alpha()
rocket_surface3 = pygame.transform.scale(rocket_surface3, (150,150))
rocket_IMGs = [rocket_surface1,rocket_surface2,rocket_surface3]
pipe_surface = pygame.image.load('sprites/pipe.png').convert_alpha()
pipe_surface = pygame.transform.scale(pipe_surface, (700,52))


class rocket:
    IMGS  = rocket_IMGs
    max_rotation = 25
    rot_vel = 20
    anim_time = 5
    

    def __init__(self ,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.width = self.x
        self.counter = 0
        self.img = self.IMGS[0]
    def jump(self):
        self.vel = -10.5###
        self.tick_count = 0
        self.width = self.x

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
        
        self.counter += 1
        if self.counter < self.anim_time:
            self.img = self.IMGS[0]
        elif self.counter < self.anim_time*2:
            self.img = self.IMGS[1]
        elif self.counter < self.anim_time*3:
            self.img = self.IMGS[2]
        elif self.counter < self.anim_time*4:
            self.img = self.IMGS[1]
        elif self.counter < self.anim_time*4 + 1:
            self.img = self.IMGS[0]
            self.counter = 0
        
        if self.tilt <= -80:
            self.img =self.IMGS[0]
            self.counter = self.anim_time*2
        # rotated_image = pygame.transform.rotate(self.img,self.tilt)
        # new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        # win.blit(rotated_image , new_rect.topleft)
        new_roc = pygame.transform.rotozoom(self.img ,self.tilt, 1)#1 is scaling factor
        roc_rect = new_roc.get_rect(center = (self.x , self.y))
        win.blit(new_roc,roc_rect)

    def get_mask(self):#collisions
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 250
    VEL = 5 ###
    
    def __init__(self,y):
        self.y = y
        self.height = 0
        
        
        self.left = 0
        self.right = 0
        self.LEFT = pygame.transform.flip(pipe_surface,True,False)
        self.RIGHT = pipe_surface
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(200,600)
        self.left = self.height - 700#self.LEFT.get_width()
        self.right = self.height +self.GAP
         
    def move(self):
        self.y += self.VEL

    def draw(self , win):
        win.blit(self.LEFT,(self.left,self.y))
        win.blit(self.RIGHT,(self.right, self.y))

    def collide(self , Rocket):
        roc_mask = Rocket.get_mask()
        LEFT_mask = pygame.mask.from_surface(self.LEFT)
        RIGHT_mask = pygame.mask.from_surface(self.RIGHT) 

        LEFT_offset = (self.left - round(Rocket.x),self.y - Rocket.y)
        RIGHT_offset = (self.right - round(Rocket.x),self.y - Rocket.y)
        
        r_point = roc_mask.overlap(RIGHT_mask,RIGHT_offset)
        l_point = roc_mask.overlap(LEFT_mask,LEFT_offset)

        if r_point or l_point :
            return True
        return False

class Base:
    VEL = 5
    LENGTH = 690
    IMG = base_surface

    def __init__(self,x):
        self.x = x
        self.y1 = 0
        self.y2 = self.LENGTH
    
    def move(self):
        self.y1 += self.VEL
        self.y2 += self.VEL

        if self.y1 > 690:
            self.y1 = -690
        
        if self.y2 > 690:
            self.y2 = -690
        
    def draw(self,win):
        win.blit(self.IMG, (self.x,self.y1))
        win.blit(self.IMG, (self.x,self.y2))
        win.blit(self.IMG, (995,self.y1))
        win.blit(self.IMG, (995,self.y2))

        


def draw_window(win, roc ,pipes ,base,score):
        win.blit(bg_surface ,(0,0))
        for pipe in pipes:
            pipe.draw(win)
            #pipe.move()
        text = STAT_FONT.render('Score: '+str(score),1,(255,255,255))
        win.blit(text,(win_width -10 - text.get_width(),10))
        base.draw(win)
        roc.draw(win)
        pygame.display.update()

def main():
    Rocket = rocket(500,520)
    base  = Base(0)
    pipes = [Pipe(-700)]
    run = True
    score = 0
    
    
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        
        #Rocket.move()
        add_pipe = False
        rem =[]
        for pipe in pipes:
            if pipe.collide(Rocket):
                pass
            if pipe.y>700:
                rem.append(pipe)
            if not pipe.passed and pipe.y > Rocket.y:
                pipe.passed = True
                add_pipe = True 
            pipe.move()
        if add_pipe:
            score += 1
            pipes.append(Pipe(-200))
        for r in rem:
            pipes.remove(r)
        if Rocket.x < -5 :
            pass
        base.move()
        draw_window(win ,Rocket,pipes,base,score)
main()
        




      