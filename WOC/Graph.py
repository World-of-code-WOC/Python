# WOC Graph.
# Module/Application de tracé graphique
#
# Auteur : World of Code
# Gmail : worldofcode.woc@gmail.com
# Github : https://github.com/World-of-code-WOC
# Site web : https://world-of-code-woc.github.io/WorldOfCode-Site/
#

import os
import sys
import time
import numpy as np

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from pygame.locals import *

def Calcul_Axes(x, y):
    """Calcul des extremums du tracé de x et y."""

    global min_x, max_x, min_y, max_y
    
    min_x = min(x) - (max(x) - min(x))*0.1
    max_x = max(x) + (max(x) - min(x))*0.1
    min_y = min(y) - (max(y) - min(y))*0.1
    max_y = max(y) + (max(y) - min(y))*0.1
    
def xy2px(Coor):
    """Converti les coordonnées d'un point du graphe en coordonnées en pixels sur pygame."""

    (X, Y) = Coor

    return round(20 + ((X - min_x)*(SIZE[0]-40))/(max_x - min_x)), round(20 + ((max_y - Y)*(SIZE[1]-40))/(max_y - min_y))

def px2xy(Pixels):
    """Converti les pixels sur pygame d'un point du graphe en coordonnées."""
    
    (X, Y) = Pixels
    
    return round((min_x + ((X - 20)*(max_x - min_x))/(SIZE[0] - 40)), 2), round((min_y + ((SIZE[1] - 20 - Y)*(max_y - min_y))/(SIZE[1] - 40)), 2)
    
def Axes():
    """Tracé des axes x = 0 et y = 0 s'ils sont visibles sur le graphe."""
    
    pos_O = xy2px((0, 0))

    if min_x < 0 < max_x:
        pygame.draw.line(fenetre, Color(255, 255, 255), (pos_O[0], 20), (pos_O[0], SIZE[1]-21))
        
    if min_y < 0 < max_y:
        pygame.draw.line(fenetre, Color(255, 255, 255), (20, pos_O[1]), (SIZE[0]-21, pos_O[1]))
        
    pygame.display.flip()
    
def Plot(X, Y, Couleur = Color(0, 0, 255), Style = ".", Epaisseur = 2):
    """Configuration du tracé."""
    
    global N, Points_x, Points_y
    
    Points_x[N] = [list(X), Couleur, Style, Epaisseur]
    Points_y[N] = [list(Y)]
    N += 1

def Trace():
    """Tracé des courbes dans la fenêtre graphique."""
    
    global Points_x, Points_y

    pygame.draw.rect(fenetre, Color(0, 0, 0), (20, 20, SIZE[0]-41, SIZE[1]-41))

    Abscisses = []
    Ordonnées = []
    
    for i in Points_x: 
        Abscisses.extend(Points_x[i][0])
        
    for j in Points_y: 
        Ordonnées.extend(Points_y[j][0])

    Calcul_Axes(Abscisses, Ordonnées)
    Axes()

    for i in Points_x:

        X = Points_x[i][0]
        Y = Points_y[i][0]
        Couleur = Points_x[i][1]
        Style = Points_x[i][2]
        Epaisseur = Points_x[i][3]
    
        if Style == ".":
        
            for j in range(len(X)):
                pygame.draw.circle(fenetre, Couleur, xy2px((X[j], Y[j])), Epaisseur)
        
        elif Style == "-":
        
            for j in range(1, len(Y)):
                pygame.draw.line(fenetre, Couleur, xy2px((X[j-1], Y[j-1])), xy2px((X[j], Y[j])), Epaisseur)
    
    Points_x = {}
    Points_y = {}

    pygame.display.flip()
    
def Show():
    """Affichage de l'interface graphique."""
    
    global fenetre, SIZE, Points_x, Points_y, N
    
    pygame.init()
    pygame.font.init()

    SIZE = (1200, 600)
    
    fenetre = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("WOC Graph.")
    Police = pygame.font.SysFont('Consolas', 15)
    
    Points_x = {}
    Points_y = {}
    N = 0

    pygame.draw.rect(fenetre, Color(255, 255, 255), (19, 19, SIZE[0]-39, SIZE[1]-39), 1)

    Trace()

    while True:

        for event in pygame.event.get():
        
            if event.type == QUIT:
                sys.exit(0)
        
        time.sleep(0.01) 

        pos_x, pos_y = pygame.mouse.get_pos()

        if 20 < pos_x < SIZE[0] - 20 and 20 < pos_y < SIZE[1] - 20:
        
            pygame.draw.rect(fenetre, Color(0, 0, 0), (SIZE[0] - 130, 0, 130, 19))
            fenetre.blit(Police.render(str(px2xy((pos_x, pos_y))), False, (255, 255, 255)), (SIZE[0] - 130, 2))
            pygame.display.flip()

def Anim(fonctions, X, Couleurs, Vitesse, Style = "-", Epaisseur = 3):
    """Affichage de fonctions avec une évolution temporelle."""
    
    global fenetre, SIZE, Points_x, Points_y, N
    
    pygame.init()
    pygame.font.init()

    SIZE = (1200, 600)
    
    fenetre = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("WOC Graph.")
    Police = pygame.font.SysFont('Consolas', 15)
    
    Points_x = {}
    Points_y = {}
    N = 0

    pygame.draw.rect(fenetre, Color(255, 255, 255), (19, 19, SIZE[0]-39, SIZE[1]-39), 1)
    
    Plot([-1, 0, 1], [-1, 0, 1], Color(255, 255, 255), ".", 2)
    Trace()

    Compteur = 0
    t = 0

    while True:

        for event in pygame.event.get():
        
            if event.type == QUIT:
                sys.exit(0)
        
        time.sleep(0.005) 
        
        Compteur += 1
        
        if Compteur % 10 == 0:
        
            t += Vitesse
            
            pygame.draw.rect(fenetre, Color(0, 0, 0), (30, 0, 200, 19))
            fenetre.blit(Police.render("t = " + str(round(t, 2)), False, (255, 255, 255)), (30, 2))

            id = 0
            
            for f in fonctions:
            
                Plot(X, f(X, t), Couleurs[id], Style, Epaisseur)
                id += 1
            
            Trace()
        
        pos_x, pos_y = pygame.mouse.get_pos()

        if 20 < pos_x < SIZE[0] - 20 and 20 < pos_y < SIZE[1] - 20:
        
            pygame.draw.rect(fenetre, Color(0, 0, 0), (SIZE[0] - 130, 0, 130, 19))
            fenetre.blit(Police.render(str(px2xy((pos_x, pos_y))), False, (255, 255, 255)), (SIZE[0] - 130, 2))
            pygame.display.flip()


if __name__ == "__main__":

    X = np.linspace(0, np.pi, 200)
    
    def f(X, t):
        return np.cos(100*t - 5*X + np.pi)
    
    Anim([f], X, [Color(0, 255, 0)], 0.001)
