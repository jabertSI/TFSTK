#Mettre le proxy
git config --global https.proxy http://10.100.100.242:80
git config --global http.proxy http://10.100.100.242:80

#Enlever le proxy
git config --global unset http.proxy 
git config --global unset https.proxy
ù
Consignes:

- Le jeu doit être écrit uniquement en python.
- 3D interdit.
- Utiliser une interface d’animation du type pygame, pytk, pygtk… (IHM 2D)
- Lorsqu’on programme avec une interface graphique, tout se déroule dans une seule boucle: la boucle d'événement.
- Callback = fonction qui se met en place lors d’un événement.
- La partie réseau est obligatoire : socket?

--- ÉTAPE 1:
 Maquette : dessiner la maquette du jeu sur une feuille de papier (dimension, toutes les vues du programme)

--- ÉTAPE 2:
Tester son programme à chaque ligne de code
Afficher fenêtre vide puis afficher vaisseau, pas a pas ..

--- ÉTAPE 3:
 Se fixer des objectifs et les tester(en interne et en externe).
À valider dans Gît après.