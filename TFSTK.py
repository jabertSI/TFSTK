import pygame
from pygame.locals import *
import random

##################################
###########INITIALISATION#########
##################################
score = 000
#PARAMETRE FENETRE DE JEUX
pygame.init()
h = 800
w = 500
screen = pygame.display.set_mode((h, w))

fond = pygame.image.load("background.jpg").convert_alpha()

WHITE = (255, 255, 255)

####################################
###########PARAMETRE SON############
####################################
son_background = pygame.mixer.Sound("sound_background.ogg")
son_background.play(loops=1, maxtime=0,fade_ms=0)
son_shoot = pygame.mixer.Sound("sfx_shoot.wav")
##########################################
#########CREATION DES LISTES##############
##########################################
#Utilisation d'une methode que j'ai trouvé sur le net qui consiste à regroupé tout les objets qui
#nécéssite un sprite à l'aide de la method Group() c'est un gain de temps est cela permet
#d'optimiser le programme et puis ça fait moins cochon ça aussi##########################
missile_list = pygame.sprite.Group()
asteroid_list = pygame.sprite.Group()
sprites_list = pygame.sprite.Group() #Groupe Sprites

#######################################
############CREATION DES OBJET#########
#######################################
### Le fait d'utiliser des objets pour notre programme va nous permettre de
# pouvoir utiliser les method de colision et de mise à jour de position. Et puis ça fait moins cochon !
#PLAYER

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.is_dead = False

    def update(self): #Utilisation de la method "update" de la lib pygame
        #La position de notre joueur se base celle du curseur
        position_player = pygame.mouse.get_pos()
        self.rect.y = position_player[1]

    def die(self):
        self.is_dead = True
        self.image = pygame.image.load('player_dead.png').convert_alpha()

# ASTEROID
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('mine.png').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= 1

# MISSILE
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('missile.png').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 3







#######################################
#######LES DIFFERENT ECRANT DU JEU####
#######################################
def menu():
    kjh = 0

def Game():
    g= 0
def end_game():
    hgf = 0
def game_over():
    gf = 0




pygame.display.flip()


def mdr():

    for event in pygame.event.get():
        if event.type == QUIT:
            game = False
        if event.type == MOUSEMOTION:
            player_y = event.pos[1]
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            game = False
        if event.type == MOUSEBUTTONDOWN:
            son_shoot.play()


    screen.blit(fond, (0, 0))



#############################################################
#############################################################
#########GOGOGOGOGOGOGOGOGOGOGOGOGOGOOGO#####################
score = 0
clock = pygame.time.Clock() #FPS
joueur = Player() #Creation joueur
sprites_list.add(joueur) #Ajout du joueur la list des sprite

asteroid_x_y = []
for i in range(10):
    asteroid = Asteroid()
    asteroid.rect.x = random.randrange(800,1000)
    asteroid.rect.y = random.randrange(100,400)
    asteroid_list.add(asteroid)
    sprites_list.add(asteroid)
    asteroid_x_y.append(asteroid.rect.x)
    asteroid_x_y.append(asteroid.rect.y)
    print(asteroid_x_y)



# BOUCLE JEU
game = True

while game:


    for k in pygame.event.get():
        if k.type == pygame.QUIT:
            game = False
        elif k.type == pygame.MOUSEBUTTONDOWN:
            misiile = Missile()
            misiile.rect.y = joueur.rect.y + 10
            misiile.rect.x = joueur.rect.x + 20
            missile_list.add(misiile)
            sprites_list.add(misiile)
            son_shoot.play()
    #Mise a jour des sprite
    sprites_list.update()

    #GEstion des liste de collision
    for misiile in missile_list:
        collide_list = pygame.sprite.spritecollide(misiile, asteroid_list, True)
        for asteroid_block in collide_list:
            missile_list.remove(misiile)
            sprites_list.remove(misiile)
            score += 1

    for asteroid in asteroid_list:
        if pygame.sprite.collide_rect(joueur,asteroid) :
            sprites_list.remove(joueur)
            if not joueur.is_dead:
                joueur.die()
            sprites_list.add(joueur)





    screen.blit(fond, (0,0))
    sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()