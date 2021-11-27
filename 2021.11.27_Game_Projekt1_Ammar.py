import pygame
import os 
import time
import random
from pygame.draw import rect

#(klasse der Einstellungen)
class Settings(object):
    window_height = 600
    window_width = 480
    FPS = 60
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file,"img")
    alien_size = (70,70)
    title="Galaxy"
    score = 0
    lives = 3
    hidden = False
    add_two = False
    add_three = False


#(klasse des Hintergrundes)
class Background(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def update(self):
        pass

#(klasse des Spielers)
class Plane(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,35))
        self.rect = self.image.get_rect()
        self.rect.left = 195
        self.rect.bottom = 600
        self.speedx = 0
        self.speedy= 0

    def update(self):
        self.speedx = 0
        self.speedy= 0
        self.keystate = pygame.key.get_pressed()
        #Tasten Bewegungssteuerung
        if self.keystate[pygame.K_LEFT]: 
            self.speedx = -8
        if self.keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.keystate[pygame.K_UP]:
            self.speedy = -8
        if self.keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.y += self.speedy
        #im Rahmen bleiben
        if self.rect.bottom > Settings.window_height:
            self.rect.bottom = Settings.window_height
        if self.rect.top < 0:
           self.rect.top = 0
        
        if self.rect.right > Settings.window_width:
            self.rect.right = Settings.window_width
        if self.rect.left < 0:
            self.rect.left = 0
#Das wird benötigt um die Lebenmöglichkeiten der Spieler
        if Settings.hidden :
            Settings.hidden = False
            self.rect.centerx = Settings.window_width / 2
            self.rect.bottom = Settings.window_height - 10


    def hide(self):
        Settings.hidden = True
        self.rect.center = (Settings.window_width/ 2, Settings.window_height + 200)


        
#(klasse der Steine)
class Stone(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.h = random.randrange(27, 65)# Größe der Steine ändern
        self.b = random.randrange(37, 62)# Größe der Steine ändern
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.b,self.h))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(Settings.window_width - self.rect.width) # um Erschaffung der Felsen an einer zufälligen Stelle oben 
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-1, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        #Im Laufe der Zeit werden die Felsen schneller und häufiger erzeugt:
        if self.rect.top > Settings.window_height + 10 or self.rect.left < -25 or self.rect.right > Settings.window_width + 20:
            if Settings.score <= 50:
                self.rect.x = random.randrange(Settings.window_width - self.rect.width)
                self.rect.y = random.randrange(-100, -40)  
                self.speedy = random.randrange(2, 5)
                Settings.add_three = True

                
            elif 50 < Settings.score <= 200:
                self.rect.x = random.randrange(Settings.window_width - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(4, 8)
                Settings.add_two= True
                if Settings.add_three == True:
                    for s in range(3): # Wenn die Bedingung erfüllt ist,erstellen 3 neue Steine
                        game.add_stone()
                    Settings.add_three= False

            elif 200 < Settings.score:
                self.rect.x = random.randrange(Settings.window_width - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(5, 10)
                if Settings.add_two == True:
                    for t in range(2):# Wenn die Bedingung erfüllt ist,erstellen 2 neue Steine
                        game.add_stone()
                    Settings.add_two= False



            Settings.score +=1
            
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)


#(klasse des Spieles)
class Game(object):
    def __init__(self)->None:
        super().__init__()
        pygame.init()
        
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        #Fotopfad
        self.background = Background("galaxy.png")
        self.plane=Plane("plane.png")
        self.stone=Stone("stone.png")
        self.running = True

        self.all_sprites=pygame.sprite.Group()
        self.stones= pygame.sprite.Group()
        self.stones.add(self.stone)
        self.all_sprites.add(self.plane) #Plane(Spieler) wird in pygame.sprite.Group-Objekten abgelegt.
        for i in range(5):
            self.add_stone()


    def add_stone(self):
        self.s = Stone("stone.png")     # das wird nochmal unten benötigt deswegen wurde Methode
        self.all_sprites.add(self.s)    #Steine wird in pygame.sprite.Group-Objekten abgelegt.
        self.stones.add(self.s)

    

    

    def run(self):
        while self.running:
            self.clock.tick(60)                              # Auf 1/60 Sekunde takten
            self.watch_for_events()
            self.update()
            self.collision()
            self.draw()
        pygame.quit()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:        # Taste unten?
                if event.key == pygame.K_ESCAPE:    # ESC gedrückt?
                    self.running = False
                elif event.key == pygame.K_x:    
                    self.running = False
            elif event.type == pygame.QUIT:         # Fenster ge-x-t?
                self.running = False

    def update(self):
        self.all_sprites.update()       # Update von allen Bitmaps

    def draw(self): # Draw von allen Bitmaps
        #Score und Lebensmöglichkeiten zu erzeugen
        self.background.draw(self.screen)
        text_score = self.font.render("Score: {0}".format(Settings.score), True, (255, 255, 0))
        self.screen.blit(text_score, dest=(10, 0))
        text_lives = self.font.render("Lives: {0}".format(Settings.lives), True, (255, 255, 0))
        self.screen.blit(text_lives, dest=(400, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


    #Kollision 
    def collision(self):
        self.hits = pygame.sprite.spritecollide(self.plane, self.stones, True, pygame.sprite.collide_circle)
        if self.hits:                # Wenn plane Kollidiert mit einem Stein
            if Settings.lives == 1 : #Wenn keine Lebensmöglichkeiten gibt, das Spiel wird beendet
                self.running = False

            elif Settings.lives > 1: # Wenn plane noch Lebensmöglichkeiten hat, wird noch mal in leben
                self.plane.hide()
                self.add_stone()
                Settings.lives-=1

        
        






if __name__ == "__main__": #Hauptprogramm starten
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"
    game=Game()
    game.run()
