import logging
import math
import operator
import numpy as np

class ConfigToolsGP():

    SELECTION_BEST                = "best"
    SELECTION_WORST               = "worst"
    SELECTION_RAND                = "rand"

    MARIAGE_BEST                  = "best"
    MARIAGE_EXTREME               = "extrem"
    MARIAGE_RAND                  = "rand"

    CROISEMENT_MIDDLE               = "swap-middle"
    CROISEMENT_ABSORPTION_PARTIELLE = "absorp-partielle"
    CROISEMENT_ABSORPTION_TOTALE    = "absorp-totale"

    MUTATION_REPLACE                = "replace"
    MUTATION_SWAP                   = "swap"
    MUTATION_DEPLACE                = "deplace"

    REMPLACEMENT_MIXT_BEST          = "mixt_best"
    REMPLACEMENT_CHILD_ONLY         = "child_only"
    REMPLACEMENT_CHILD_ADD          = "child_add"
    REMPLACEMENT_MIXT_RAND          = "mixt_rand"


 
    """
    Classe de configuration pour l'algorithme de programmation génétique.
    Elle initialise les paramètres par défaut et permet leur modification via une instance d'ArgParseToolsGP.
    """
    def __init__(self,params):
        """
        Initialise l'instance de configuration avec des valeurs par défaut.
        Args:
            params (ArgParseToolsGP): Instance contenant les paramètres personnalisés.
        """
        self.funct_binaire = ['+', '-', '*', '**', '/'] # Fonctions binaires disponibles.
        self.funct_unaire  = ['sin','cos','ln','sqrt','tan','ctg','e','tanh','abs'] # Fonctions unaires disponibles.
        self.functions     = {'+':operator.add,
                              '-':operator.sub,
                              '*':operator.mul,
                              '**':np.power,
                              '/':np.divide,
                              'sin':np.sin,
                              'cos':np.cos,
                              'ln':np.log,
                              'sqrt':np.sqrt,
                              'tan':np.tan,
                              'ctg':lambda x:1/np.tan(x),
                              'e':np.exp,
                              'tanh':np.tanh,
                              'abs':np.abs
                              }
        self.terminal_set  = ['x']

        self.modes_selection    = ( ( "Sélectionner l'échantillon avec les meilleurs ",self.SELECTION_BEST),
                                    ( "Sélectionner l'échantillon  avec les pires ",self.SELECTION_WORST),
                                    ( "Sélectionner l'échantillon  de façon aléatoire",self.SELECTION_RAND)
                                   )
        self.modes_mariage      = ( ("Mariage des meilleures successif",self.MARIAGE_BEST),
                                      ("Mariage des meilleures avec les pires",self.MARIAGE_EXTREME),
                                      ("Mariage aléatoire",self.MARIAGE_RAND)
                                   )
        self.modes_croisement   = ( ("Croisement avec échange d'un bloc génétique",self.CROISEMENT_MIDDLE),
                                    ("Croisement avec absorption partielle",self.CROISEMENT_ABSORPTION_PARTIELLE),
                                    ("Croisement avec absorption totale ",self.CROISEMENT_ABSORPTION_TOTALE)
                                  )
        self.modes_remplacement = ( ( "Mélanger parents et enfants pour choisir les meilleurs",self.REMPLACEMENT_MIXT_BEST),
                                    ( "Les enfants seulement",self.REMPLACEMENT_CHILD_ONLY),
                                    ( "Ajouter les enfants aux parents",self.REMPLACEMENT_CHILD_ADD),
                                    ( "Mélanger parents et enfants pour choisir de façon aléatoire",self.REMPLACEMENT_MIXT_RAND)
                                   )
        self.modes_mutation     = ( ( "Remplacer un gène ",self.MUTATION_REPLACE),
                                    ( "Intervertir deux gènes",self.MUTATION_SWAP),
                                    ( "Déplacer un gène ",self.MUTATION_DEPLACE)
                                  )
        self.config=False
        self.formule="x**2+x*sin(x)"     # Formule initiale.
        self.xmin=0                      # Valeur minimale de x.
        self.xmax=10                     # Valeur maximale de x.
       
        self.seuil_fitness=0.01          # Seuil de fitness pour arrêter l'algorithme.
        self.tolerance_gene_Length=0.5   # Tolérance pour la longueur génétique.
        self.tolerance_gene_Mutate=0.5   # Tolérance pour la mutation génétique.

        self.mode_selection   =self.SELECTION_BEST          # mode de sélection.
        self.mode_mariage     =self.MARIAGE_EXTREME         # mode de mariage.
        self.mode_croisement  =self.CROISEMENT_MIDDLE       # mode de croisement.
        self.mode_remplacement=self.REMPLACEMENT_MIXT_BEST  # mode de remplacement.
        self.mode_mutation    =self.MUTATION_REPLACE        # mode de mutation.

        self.size_echantillon = 100      # Taille de l'échantillon.
        self.max_depth = 5               # Profondeur maximale de l'arbre génétique.
        self.size_population = 1000      # Taille de la population.
        self.max_iterations=1000         # Nombre maximal d'itérations.
        self.max_N_valeur=10             # Valeur maximale des constantes.
        self.duree_maximum=60*60*24      # Durée maximale d'exécution (en secondes).
        self.verbose=False               # Mode verbeux désactivé par défaut.
        self.dlg2d=False                 # Mode 2d désactivé par défaut.
        self.seed=123456789              # Graine pour l'initialisation aléatoire.
        self.fichier_populate=""         # Fichier de population (vide par défaut).
        self.startValue=0                # Valeur de départ pour l'algorithme.
        self.horizon=0                   # Horizon pour l'algorithme.
        if params!=None :
            self.initialise(params)

    def initialise(self,params):
        """
        Initialise les paramètres avec les valeurs fournies par une instance d'ArgParseToolsGP.
        Args:
            params (ArgParseToolsGP): Instance contenant les paramètres personnalisés.
        """

        self.size_population=params.size_population
        self.max_depth=params.size_depth
        self.size_echantillon=params.size_echantillon 
        self.max_N_valeur=params.max_N_valeur
        self.max_iterations=params.nb_iterations
        self.duree_maximum=params.duree_maximum
        self.xmin=params.xmin
        self.xmax=params.xmax



        self.mode_mariage=params.mariage
        self.mode_croisement=params.croisement
        self.mode_selection=params.selection
        self.mode_remplacement=params.remplacement
        self.mode_mutation=params.mutation

        self.seed=params.seed
        if params.formule!="" :
            self.formule=params.formule
        self.verbose=params.verbose
        self.bl_thread=params.bl_thread

        self.seuil_fitness=params.seuil_fitness
        self.tolerance_gene_Length=params.tolerance_gene_Length
        self.tolerance_gene_Mutate=params.tolerance_gene_Mutate

        self.fichier_populate=params.population_file

        # Manage logging
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG if self.verbose else logging.INFO)

    def info(self,message):
        logging.info(message)

    def error(self,message):
        logging.error(message)
