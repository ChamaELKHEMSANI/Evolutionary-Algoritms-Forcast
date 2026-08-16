import sys
import random
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from tools.mathsToolsGP import MathsToolsGP 
 
class DrawToolsGP():
    """
    Classe contenant les outils mathématiques pour afficher des graphes.
    Elle fournit des méthodes pour générer des terminaux, évaluer des fonctions unaires et binaires,
    et manipuler des gènes sous forme de chaînes de caractères.
    """
    def __init__(self):
        pass

    def draw_surface_1(X, Y,formule):
        """
        Affiche une surface 3D en fonction d'une formule et des valeurs X, Y.
        Args:
            X (list): Liste des valeurs X.
            Y (list): Liste des valeurs Y.
            formule (str): La formule à évaluer.
        """
        Z = np.empty((len(X),len(Y)), dtype=float)
        for i   in range(len(X)):
            for j in range(len(Y)):
                Z[i,j]=MathsToolsGP.evaluate_formule(formule,x=X[i],y=Y[j])
        
        plt.style.use('_mpl-gallery')    
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        X, Y = np.meshgrid(X, Y)
        # Plot 
        ax.plot_surface(X, Y, Z,vmin=Z.min(), cmap=cm.Blues)#formule1
        plt.show()

    def draw_surface_2(X, Y,formule1,formule2):
        """
        Affiche deux surfaces 3D en fonction de deux formules et des valeurs X, Y.
        Args:
            X (list): Liste des valeurs X.
            Y (list): Liste des valeurs Y.
            formule1 (str): La première formule à évaluer.
            formule2 (str): La seconde formule à évaluer.
        """
        Z1 = np.empty((len(X),len(Y)), dtype=float)
        Z2 = np.empty((len(X),len(Y)), dtype=float)
        for i   in range(len(X)):
            for j in range(len(Y)):
                Z1[i,j]=MathsToolsGP.evaluate_formule(formule1,x=X[i],y=Y[j])
                Z2[i,j]=MathsToolsGP.evaluate_formule(formule2,x=X[i],y=Y[j])
        
        plt.style.use('_mpl-gallery')    
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        X1, Y1 = np.meshgrid(X, Y)
        # Plot 
        ax.plot_surface(X1, Y1, Z1,vmin=Z1.min(), cmap=cm.Blues)#formule1
        ax.plot_surface(X1, Y1, Z2,vmin=Z2.min(), cmap=cm.Greens)#formule2
        plt.show()

    def draw_surface_fichier(inputfile):
        """
        Affiche une surface 3D basée sur des données lues depuis un fichier.
        Args:
            inputfile (str): Le fichier contenant les données à afficher.
        """
        valeurs = []
        with open(inputfile, 'r') as file:
            line_list = file.readlines()
        for line in line_list:
            vals = line.strip().split(';')
            valeurs.append([float(vals[0]), float(vals[1]), float(vals[2])])

        x = [row[0] for row in valeurs]
        y = [row[1] for row in valeurs]
        X = np.unique(x)
        Y = np.unique(y)
        tab_x = X.tolist()
        tab_y = Y.tolist()
        X, Y = np.meshgrid(tab_x, tab_y)
        Z = np.empty((len(tab_y), len(tab_x)), dtype=float)
        for val in valeurs:
            Z[tab_y.index(val[1]), tab_x.index(val[0])] = val[2]

        plt.style.use('_mpl-gallery')
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        # Plot
        ax.plot_surface(X, Y, Z, vmin=Z.min(), cmap=cm.Blues)
        plt.show()

    def draw_resultats(X,Y,field_x,field_y,titre):
        """
        Affiche un resultat en fonction de deux formules et des valeurs X, Y.
        Args:
            X (list): Liste des valeurs X.
            Y (list): Liste des valeurs Y.
            titre (str): titre de la représentation.
         """

        fig, ax = plt.subplots()
        plt.title(titre)
        ax.set_xlabel(field_x)
        ax.set_ylabel(field_y)
        plt.plot(X,Y,"o-")
        plt.show()  
