import pygame
from pygame.locals import *
import random
import math
# random permet de tirer un chiffre aléatoirement


##################################
###########INITIALISATION#########
##################################
score = 000
#PARAMETRE FENETRE DE JEUX
pygame.init()
w = 800
h = 500
x = 0
y = 0
x1 = 0
y1 = -w
screen = pygame.display.set_mode((w, h)) #Fenêtre
pygame.display.set_caption('TWENTY FIVE SECONDS TO KILL')
clock = pygame.time.Clock() #FPS et timer

fond = pygame.image.load("background.gif").convert_alpha() # convert alpha pour rendre transparent
#Définition des couleurs pour affichage des textes:
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = ((255, 67, 0))
ORANGE_LOW = (237, 193, 177)
BLUE =(0, 191, 255)
OR = (249, 223, 22)
####################################
###########PARAMETRE SON############
####################################
son_background = pygame.mixer.Sound("sound_background.ogg")
son_background.play(loops=1, maxtime=0,fade_ms=0)
son_shoot = pygame.mixer.Sound("sfx_shoot.wav") #le module mixer permet de jouer les sons
son_boom_a = pygame.mixer.Sound("asteroid_boom.wav")
son_boom_p = pygame.mixer.Sound("player_boom.wav")
font_game = pygame.font.match_font('Bold')
#Sors une police en gras (bold) qui diffère en fonction du pc qui lance le programme

##########################################
#########CREATION DES LISTES##############
##########################################

missile_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
sprites_list = pygame.sprite.Group() #Groupe Sprites qui met tous les objets similaires à rafraichir dans une liste.
pygame.mouse.set_visible(0) #Cacher le curseur de la souris

#######################################
############CREATION DES OBJET#########
#######################################
### Le fait d'utiliser des objets pour notre programme va nous permettre de
# pouvoir utiliser les méthodes de colision et de mise à jour de position. Et puis ça fait plus propre !

#PLAYER

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.is_dead = False
#__init__ est un constructeur et self correspond aux paramètres. rect permet de faire un rectangle et
# super permet de récupérer un objet déjà existant.
    def update(self): #Utilisation de la methode "update" de la librairie pygame
        #La position de notre joueur se base sur celle du curseur
        position_player = pygame.mouse.get_pos() #Prend la position du curseur
        self.rect.y = position_player[1] - 12 #Prend le point y du cursor - 12 pixel afin que le vaisseau soit centré


    def die(self):
        self.is_dead = True
        self.image = pygame.image.load('player_dead.png').convert_alpha()
#Affichage du player après explosion


# ENEMY
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.speedx = random.randrange(1, 4)
        self.speedy = (random.randrange(1,4))
    #speed = paramètre de vitesse aléatoire entre 1 et 4
    # random = prend un chiffre et randrange = donne l'intervalle

    def enemy_spawn():
        for i in range(2):
            enemy = Enemy()
            enemy.rect.x = random.randrange(800, 1000)
            enemy.rect.y = random.randrange(100, 450)
            enemy_list.add(enemy)
            sprites_list.add(enemy)

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.bottom > h:
            self.rect.x = random.randrange(800, 1000)
            self.rect.y = random.randrange(100, 460)
            self.speedx += random.randrange(1, 4)
            self.speedy += (-3,3)

#position du joueur se fie à la vitesse.

# MISSILE
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('missile.png').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 7
#Avance de 7 pixel à chaque raffraichissement.

#Fonction text :
def text_draw(surf,text, size,x,y, color):
    font = pygame.font.Font(font_game,size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect) #Raffraichir pour afficher (écrit, rectangle)
#Définir les paramètres puis leur donner définition

#######################################
#######LES DIFFERENTS ECRANS DU JEU####
#######################################
def menu():
    screen.blit(fond, (x, y))

    text_draw(screen, "TWENTY FIVE", 60, w / 2, 100, BLUE)
    text_draw(screen, "SECONDS TO", 60, w / 2, 140, BLUE)
    text_draw(screen, "KILL", 100, w / 2, 170, RED)
    text_draw(screen, "SPACE to START", 40, w / 2, 300,OR)
    text_draw(screen, "ESCAPE to QUIT", 40, w / 2, 340,OR)
def best_score():

    text_draw(screen, "Press SPACE to restart or ESCAPE to quit", 40, w / 2, 450, WHITE)
    text_draw(screen, str(score), 80, w / 2, 300, ORANGE)
    text_draw(screen, "Congratulations, you got the highest score in the world", 40, w / 2, 200,OR)
def end_game():

    text_draw(screen, "TIME'S UP", 80, w / 2, h / 2, ORANGE_LOW)
    text_draw(screen, "Press SPACE to restart or ESCAPE to quit", 40, w / 2, 450, WHITE)
    text_draw(screen, str(score), 80, w / 2, 300, ORANGE)
def game_over():

    text_draw(screen, "You are DEAD", 80, w / 2, h / 2, ORANGE_LOW)
    text_draw(screen, "Press SPACE to restart or ESCAPE to quit", 40, w / 2, 450, WHITE)
    text_draw(screen, str(score), 80, w / 2, 300, ORANGE)
#############################################################
#############################################################
#########GOGOGOGOGOGOGOGOGOGOGOGOGOGOOGO#####################
score = 0
enemy_cpt = 0
enemy_empty = False
alive = True

joueur = Player() #Creation joueurs
sprites_list.add(joueur) #Ajout du joueur à la liste des sprites

# BOUCLE JEU
game = True
round = False
end_round = False
first_time = True

while game:
    print(enemy_cpt)

    if not round and not end_round:
        menu()
        for p in pygame.event.get():
            if p.type == KEYDOWN and p.key == K_SPACE:
                round=True
            if p.type == pygame.QUIT or p.type == KEYDOWN and p.key == K_ESCAPE:
                game = False
    else:
        if first_time:
            time = pygame.time.get_ticks()
            first_time = False

        seconds = 25 - (pygame.time.get_ticks() - time) // 1000

        y += 2
        y1 += 2
        for k in pygame.event.get():
            if k.type == pygame.QUIT  or k.type == KEYDOWN and k.key == K_ESCAPE:
                #Enfoncer la touche échap pour quitter
                game = False
            elif k.type == pygame.MOUSEBUTTONDOWN and alive and not end_round:
                misiile = Missile()
                misiile.rect.y = joueur.rect.y + 10
                misiile.rect.x = joueur.rect.x + 50
                missile_list.add(misiile)
                sprites_list.add(misiile)
                son_shoot.play()

        #Mise a jour des sprites
        sprites_list.update()

        #Gestion des liste de collision
        for misiile in missile_list:
            collide_list = pygame.sprite.spritecollide(misiile, enemy_list, True)
            for enemy_block in collide_list:
                missile_list.remove(misiile)
                sprites_list.remove(misiile)
                son_boom_a.play()
                score += 1
                enemy_cpt -= 1
                if enemy_cpt < 7:  #Les ennemis sont générés par l'utilisateur, il crée sa propre dificulté
                    Enemy.enemy_spawn()
            if misiile.rect.x > 800: #ON check si le missile sort de l'écran
                missile_list.remove(misiile)
                sprites_list.remove(misiile)



        for a in enemy_list:
            if a.rect.x < 0: #On test si l'ennemi sort de l'écran
                enemy_list.remove(a)
                enemy_cpt -= 1

            if pygame.sprite.collide_rect(joueur,a) and a.rect.x >= 60:
                alive = False
                sprites_list.remove(joueur)
                enemy_list.empty()
                son_boom_p.play()
                son_background.stop()
                sprites_list.empty()
                first_time = False
                if not joueur.is_dead:
                    joueur.die()
                sprites_list.add(joueur)


        #On verifie qu'il y des enemy présent sur la map, au cas où si le joueur n'en tue pas afin de pouvoir en régénérer
        if enemy_cpt <= 3:
            enemy_empty = True
        else:
            enemy_empty = False
        if enemy_empty:
            for loop in range(5):
                Enemy.enemy_spawn()
                enemy_cpt += 2

        screen.blit(fond, (y,x)) #screen.blit = clignoter, raffraichir
        screen.blit(fond,(y1,x1))
        if y > w:
            y = -w
        if y1 > w:
            y1 = -w

        sprites_list.draw(screen)
        #Dessine tous les sprites dans la fenêtre
        if alive == True and end_round == False:
            text_draw(screen, str(score), 80, w / 2, 10, ORANGE) #str permet de convertir en chaîne de caractère
            text_draw(screen, str(seconds), 80, 700, 10, BLUE)
            text_draw(screen, "sec", 50, 760, 26, WHITE)

        elif alive == False:
            game_over()
            if k.type == KEYDOWN and k.key == K_SPACE:
                alive = True
                score = 0
                son_background.play()
                sprites_list.remove(joueur)
                joueur = Player()
                sprites_list.add(joueur)
                first_time = True
                round=False
                for loop in range(5):
                    Enemy.enemy_spawn()
            elif k.type == KEYDOWN and k.key == K_ESCAPE:
                game = False
        if seconds < 0:
            end_round = True
            sprites_list.empty()
            enemy_list.empty()
            enemy_cpt = 0
            end_game()
            if k.type == KEYDOWN and k.key == K_ESCAPE:
                game = False

            elif k.type == KEYDOWN and k.key == K_SPACE:
                end_round = False
                round=False
                first_time = True
                joueur = Player()
                sprites_list.add(joueur)
                score = 0


    pygame.display.flip()
    # display.flip correspond au raffraichissement de la fenêtre en entier.
    clock.tick(60)
    #Fréquence du jeu

pygame.quit()

