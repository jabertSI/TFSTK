import random
import socket

import pygame
from pygame.locals import *

import eztext
import pyganim

# random permet de tirer un chiffre aléatoirement


###################################
###########INITIALISATION#########
##################################
pseudo = ""
score = 0
# PARAMETRE FENETRE DE JEUX
pygame.init()
w = 800
h = 500
x = 800
y = 0

screen = pygame.display.set_mode((w, h))  # Fenêtre
pygame.display.set_caption('TWENTY FIVE SECONDS TO KILL')
clock = pygame.time.Clock()  # FPS et timerl

fond = pygame.image.load("template\galaxy.png")  # convert alpha pour rendre transparent
# Définition des couleurs pour affichage des textes:
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (232, 101, 59)
ORANGE_LOW = (237, 193, 177)
PAL = (45, 16, 0)
BLUE = (115, 151, 194)
NAVY_BLUE = (160, 229, 255)
OR = (249, 223, 22)
####################################

###########PARAMETRE SON############
####################################
son_background = pygame.mixer.Sound("template\sounds\sound_background.ogg")
son_background.play(loops=1, maxtime=0, fade_ms=0)
son_shoot = pygame.mixer.Sound("template\sounds\sfx_shoot.wav")  # le module mixer permet de jouer les sons
son_boom_a = pygame.mixer.Sound("template\sounds\emy_boom.wav")
son_boom_p = pygame.mixer.Sound("template\sounds\player_boom.wav")
font_game = pygame.font.match_font('Bold')
# Sors une police en gras (bold) qui diffère en fonction du pc qui lance le programme

##########################################
#########CREATION DES LISTES##############
##########################################

missile_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
sprites_list = pygame.sprite.Group()  # Groupe Sprites qui met tous les objets similaires à rafraichir dans une liste.
pygame.mouse.set_visible(0)  # Cacher le curseur de la souris


#######################################
############CREATION DES OBJET#########
#######################################
### Le fait d'utiliser des objets pour notre programme va nous permettre de
# pouvoir utiliser les méthodes de colision et de mise à jour de position. Et puis ça fait plus propre !

# PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('template\character\player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.is_dead = False

        # __init__ est un constructeur et self correspond aux paramètres. rect permet de faire un rectangle et

    # super permet de récupérer un objet déjà existant.
    def update(self):  # Utilisation de la methode "update" de la librairie pygame
        # La position de notre joueur se base sur celle du curseur
        # Prend la position du curseur
        # Prend le point y du cursor - 12 pixel afin que le vaisseau soit centré
        if self.is_dead:
            position_player = last_pos
            self.rect.y = position_player[1]
        else:
            position_player = pygame.mouse.get_pos()

            if position_player[1] > 80 and position_player[1] < 474:
                self.rect.y = position_player[1] - 12

    def die(self):

        self.is_dead = True
        #self.image = pygame.image.load('template\character\player_dead.png').convert_alpha()


player_explo = pyganim.PygAnimation([('template/explo/ship/bubble_explo1.png', 0.1),
                                     ('template/explo/ship/bubble_explo3.png', 0.1),
                                     ('template/explo/ship/bubble_explo3.png', 0.1),
                                     ('template/explo/ship/bubble_explo4.png', 0.1),
                                     ('template/explo/ship/bubble_explo5.png', 0.1),
                                     ('template/explo/ship/bubble_explo6.png', 0.1),
                                     ('template/explo/ship/bubble_explo7.png', 0.1),
                                     ('template/explo/ship/bubble_explo8.png', 0.1),
                                     ('template/explo/ship/bubble_explo9.png', 0.1),
                                     ('template/explo/ship/bubble_explo10.png', 0.1)], loop=False)


# ENEMY
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        rand_enemy = random.randrange(1, 8)

        if rand_enemy == 1:
            self.image = pygame.image.load('template\character\enemy_y.png').convert_alpha()
        elif rand_enemy == 2:
            self.image = pygame.image.load('template\character\enemy_o.png').convert_alpha()
        elif rand_enemy == 3:
            self.image = pygame.image.load('template\character\enemy_p.png').convert_alpha()
        elif rand_enemy == 4:
            self.image = pygame.image.load('template\character\enemy_p.png').convert_alpha()
        else:
            self.image = pygame.image.load('template\character\enemy_g.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.speedx = (random.randrange(3, 5))
        self.speedy = (random.randrange(1, 4))

    # speed = paramètre de vitesse aléatoire entre 1 et 4
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


enemy_explo = pyganim.PygAnimation([('template/explo/enemy/enemy_explo1.png', 0.1),
                                    ('template/explo/enemy/enemy_explo3.png', 0.1),
                                    ('template/explo/enemy/enemy_explo3.png', 0.1),
                                    ('template/explo/enemy/enemy_explo4.png', 0.1),
                                    ('template/explo/enemy/enemy_explo5.png', 0.1),
                                    ('template/explo/enemy/enemy_explo6.png', 0.1),
                                    ('template/explo/enemy/enemy_explo7.png', 0.1),
                                    ('template/explo/enemy/enemy_explo8.png', 0.1)], loop=False)


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('template\character\oss.png').convert_alpha()
        self.rect = self.image.get_rect()

    def Boss_spawn():
        son_bosse = pygame.mixer.Sound("template\sounds\evil.ogg")
        son_bosse.play()
        bigboss = Boss()
        bigboss.rect.x = 800
        bigboss.rect.y = 50
        sprites_list.add(bigboss)
        enemy_list.add(bigboss)

    def update(self):

        if self.rect.x == 350:
            pass
        else:
            self.rect.x -= 5



# MISSILE
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('template\weap\missile.png').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 7
        # Avance de 7 pixel à chaque raffraichissement.


# Fonction communication avec le server
def PutScore(bool):
    copi_c = bool
    bool_test = False

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(("localhost", 1111))  # ip + port du serveur
    cmd = "putScore"  # Commande à envoyé au serveur
    first_cmd = True
    if not copi_c:
        c.send(cmd.encode())  # la fonction send envoie la cmd au serveur après l'avoir encode
        y = c.recv(9999999)  # reception
        NickScore = pseudo + " " + str(score)
        if y == b'dropNickSc':
            c.send(NickScore.encode())
        y = c.recv(9999999)
        if y == b'a':
            print('best score')
            return 1
        else:
            print('not the best score')
            return 0


# Fonction text :
def text_draw(surf, text, size, x, y, color):
    font = pygame.font.Font(font_game, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)  # Raffraichir pour afficher (écrit, rectangle)


# Définir les paramètres puis leur donner définition
def bx(nickname):
    fgh = True
    txtbx = eztext.Input(x=50, y=50, maxlength=10, color=(PAL), prompt='Enter your Nickname: ')
    while fgh:
        # make sure the program is running at 30 fps
        # events for txtbx
        events = pygame.event.get()
        # process other events

        for event in events:

            # close it x button si pressed
            if event.type == QUIT:
                quit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                nickname = txtbx.value
                return nickname
                fgh = False

        # clear the screen
        screen.fill(NAVY_BLUE)
        # update txtbx
        txtbx.update(events)
        # blit txtbx on the sceen
        txtbx.draw(screen)
        # refresh the display
        pygame.display.flip()


#######################################
#######LES DIFFERENTS ECRANS DU JEU####
#######################################
def menu():
    screen.fill(NAVY_BLUE)
    text_draw(screen, "TWENTY FIVE", 60, w / 2, 100, PAL)
    text_draw(screen, "SECONDS TO", 60, w / 2, 140, PAL)
    text_draw(screen, "KILL", 100, w / 2, 170, RED)
    text_draw(screen, "SPACE to START", 40, w / 2, 300, WHITE)
    text_draw(screen, "ESCAPE to QUIT", 40, w / 2, 340, WHITE)


def best_score():
    text_draw(screen, "Press SPACE to restart or ESCAPE to quit", 40, w / 2, 450, WHITE)
    text_draw(screen, str(score), 80, w / 2, 300, ORANGE)
    text_draw(screen, "Congratulations, you got the highest score in the world", 40, w / 2, 200, OR)


def end_game():
    text_draw(screen, "TIME'S UP", 80, w / 2, h / 2, ORANGE_LOW)
    text_draw(screen, "Press SPACE to restart or ESCAPE to quit", 40, w / 2, 450, WHITE)
    text_draw(screen, str(score), 80, w / 2, 300, ORANGE)


def game_over():
    text_draw(screen, "You are DEAD", 80, w / 2, h / 2, ORANGE_LOW)
    text_draw(screen, "Press SPACE to restart or ESCAPE to quit", 40, w / 2, 450, WHITE)
    text_draw(screen, str(score), 80, w / 2, 300, ORANGE)


def GUI():
    text_draw(screen, str(score), 80, w / 2, 10, ORANGE)  # str permet de convertir en chaîne de caractère
    text_draw(screen, str(seconds), 80, 700, 10, BLUE)
    # text_draw(screen, "sec", 50, 760, 26, WHITE)


#############################################################
#############################################################
#########GOGOGOGOGOGOGOGOGOGOGOGOGOGOOGO#####################
# Boucle de jeu
enemy_cpt = 0
enemy_empty = False
alive = True

joueur = Player()  # Creation joueurs
sprites_list.add(joueur)  # Ajout du joueur à la liste des sprites

game = True
round = False
end_round = False
first_time = True
score_send = False
score_result = -1
last_pos = 0, 0
last_pos_enemy = 0, 0
nick = False
while game:
    if not round and not end_round and not nick:
        menu()
        for p in pygame.event.get():
            if p.type == KEYDOWN and p.key == K_SPACE:
                round = True
                nick = True
                if round and not end_round and nick:
                    # bx(pseudo)
                    pseudo = bx(pseudo)
            if p.type == pygame.QUIT or p.type == KEYDOWN and p.key == K_ESCAPE:
                game = False




    else:

        if first_time:
            time = pygame.time.get_ticks()
            first_time = False

        seconds = 25 - (pygame.time.get_ticks() - time) // 1000

        for k in pygame.event.get():
            if k.type == pygame.QUIT or k.type == KEYDOWN and k.key == K_ESCAPE:
                # Enfoncer la touche échap pour quitter
                game = False
            elif k.type == pygame.MOUSEBUTTONDOWN and alive and not end_round:
                misiile = Missile()
                misiile.rect.y = joueur.rect.y + 10
                misiile.rect.x = joueur.rect.x + 50
                missile_list.add(misiile)
                sprites_list.add(misiile)
                son_shoot.play()

        # Mise a jour des sprites
        sprites_list.update()

        # Gestion des liste de collision
        for misiile in missile_list:
            collide_list = pygame.sprite.spritecollide(misiile, enemy_list, True)
            for enemy_block in collide_list:
                last_pos_enemy = (misiile.rect[0], misiile.rect[1])
                missile_list.remove(misiile)
                sprites_list.remove(misiile)
                son_boom_a.play()
                score += 1
                enemy_cpt -= 1
                enemy_explo.play()
                if enemy_cpt < 4 and not end_round:  # Les ennemis sont générés par l'utilisateur, il crée sa propre dificulté
                    Enemy.enemy_spawn()
            if misiile.rect.x > 800:  # ON check si le missile sort de l'écran
                missile_list.remove(misiile)
                sprites_list.remove(misiile)

        for a in enemy_list:
            if a.rect.x < 0 and not end_round:  # On test si l'ennemi sort de l'écran
                enemy_list.remove(a)
                enemy_cpt -= 1

            if pygame.sprite.collide_rect(joueur, a) and a.rect.x >= 30:
                alive = False
                sprites_list.remove(joueur)
                enemy_list.empty()
                missile_list.empty()
                son_boom_p.play()
                son_background.stop()
                sprites_list.empty()
                first_time = False
                last_pos = pygame.mouse.get_pos()
                Boss.Boss_spawn()

                if not joueur.is_dead:
                    joueur.die()
                    player_explo.play()
                    # sprites_list.add(joueur)

        # On verifie qu'il y des enemy présent sur la map, au cas où si le joueur n'en tue pas afin de pouvoir en régénérer
        if enemy_cpt <= 3:
            enemy_empty = True
        else:
            enemy_empty = False
        if enemy_empty and not end_round:
            for loop in range(5):
                Enemy.enemy_spawn()
                enemy_cpt += 2

        screen.blit(fond, (x, 0))  # screen.blit = clignoter, raffraichir
        screen.blit(fond, (x - w, 0))
        x -= 1

        if x == -w:
            x = 800

        sprites_list.draw(screen)
        # Dessine tous les sprites dans la fenêtre
        if alive == True and not end_round:
            GUI()


        elif alive == False:
            game_over()

            if score_result == -1:
                try:
                    score_result = PutScore(score_send)

                except Exception:
                    score_result = 2
                    player_explo.play()
                    print('connexion failed')

            if score_result == 1:
                best_score()

            if k.type == KEYDOWN and k.key == K_SPACE:
                enemy_list.empty()
                sprites_list.empty()
                x = 800
                score_result = -1
                alive = True
                score_send = False
                score = 0
                son_background.play()
                sprites_list.remove(joueur)
                joueur = Player()
                sprites_list.add(joueur)
                first_time = True
                round = False

                for loop in range(5):
                    Enemy.enemy_spawn()
            elif k.type == KEYDOWN and k.key == K_ESCAPE:
                game = False
        if seconds < 0 and alive:
            son_background.stop()
            end_round = True
            sprites_list.empty()
            enemy_list.empty()
            enemy_cpt = 0
            end_game()
            son_background.stop()

            if score_result == -1:
                try:
                    score_result = PutScore(score_send)

                except Exception:
                    score_result = 2
                    print('connexion failed')

            if score_result == 1:
                best_score()
            if k.type == KEYDOWN and k.key == K_ESCAPE:
                game = False

            elif k.type == KEYDOWN and k.key == K_SPACE:
                score_result = -1
                x = 800
                end_round = False
                round = False
                first_time = True
                joueur = Player()
                sprites_list.add(joueur)
                score = 0
                son_background.play()

    player_explo.blit(screen, (0, last_pos[1]))
    enemy_explo.blit(screen, (last_pos_enemy))

    pygame.display.flip()
    # display.flip correspond au raffraichissement de la fenêtre en entier.
    clock.tick(60)
    # Fréquence du jeu

pygame.quit()
