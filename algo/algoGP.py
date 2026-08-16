import sys
import warnings
import random
import time
import numpy as np

from algo.chromosomeGP import ChromosomeGP
from tools.configToolsGP import ConfigToolsGP
from algo.geneGP import GeneGP

warnings.filterwarnings("ignore")
"""
La classe AlgoGP implémente un algorithme génétique programmatique (AGP),:

1. Attributs de la classe (__init__)
config: Paramètres de configuration pour l'algorithme.
population: Liste des individus de la population actuelle.
new_population: Liste des nouveaux individus générés lors de chaque itération.
inputs et outputs: Données d'entrée et résultats cibles de la fonction à optimiser.
widget: Interface graphique associée pour le suivi de l'avancement.
isRunning: Indicateur pour savoir si l'algorithme est en cours d'exécution.
elapsed_time: Temps écoulé depuis le démarrage de l'algorithme.
2. Méthodes principales
- initialise(self, config, inputs, outputs, widget)
Initialise les paramètres de l'algorithme, y compris les outils mathématiques, les données d'entrée/sortie, et l'interface graphique. Si un "seed" est spécifié, il est utilisé pour initialiser les générateurs aléatoires. Les tailles de l'échantillon et de la population sont également ajustées ici.

- populate_generate(self)
Crée une population initiale d'individus en utilisant des chromosomes générés de manière aléatoire. Pour chaque individu, l'algorithme calcule la "fitness" (qualité de la solution) en fonction des données d'entrée et de sortie. Si un individu a une "fitness" invalide, il est régénéré jusqu'à ce qu'un individu valide soit trouvé.

- populate_read(self, fichier)
Charge la population à partir d'un fichier, en lisant chaque ligne et en initialisant les chromosomes correspondants.

- populate_write(self, fichier)
Sauvegarde la population actuelle dans un fichier, chaque chromosome étant écrit au format approprié.

- populate(self)
Initialise la population soit par génération aléatoire, soit en la chargeant depuis un fichier, selon la configuration.

- execute(self)
Exécute l'algorithme génétique, en procédant par itérations. Chaque itération comprend une sélection des meilleurs individus, la reproduction (croisement) et la mutation pour générer la nouvelle population. L'algorithme s'arrête lorsqu'un critère d'arrêt est atteint (nombre maximal d'itérations, seuil de fitness, durée maximale, ou si l'algorithme est arrêté manuellement).

- echantillon_range(self)
Sélectionne un sous-ensemble d'individus de la population en effectuant un tirage au sort, puis trie ces individus en fonction de leur fitness.

- iterate_generation(self, iteration)
Gère une itération complète de l'algorithme, où les individus sont croisés pour produire une nouvelle génération. Les individus les plus "fit" sont sélectionnés, croisés et mutés, puis ajoutés à la nouvelle population.

- insert_child(self, child, iteration)
Insère un enfant dans la nouvelle population, en effectuant éventuellement une mutation et en calculant sa fitness. Si l'enfant est valide, il est ajouté à la population.

- isStop(self)
Renvoie un booléen indiquant si l'algorithme doit s'arrêter (basé sur l'attribut isRunning).

- setAvancement(self, str_message, pos_value, max_value)
Met à jour l'interface graphique avec l'état d'avancement de l'algorithme. Utilise le widget pour afficher le progrès sous forme de jauge.

- affiche_resultats(self)
Affiche les résultats de l'algorithme à l'aide du widget.

- get_best(self)
Récupère l'individu le plus "fit" de la population actuelle (celui avec la meilleure fitness).




"""
class AlgoGP():


    def __init__(self):
        """
        Initialise l'instance de l'algorithme génétique programmatique.
        """
        # Initialisation des attributs de l'algorithme
        self.config=None                    # Paramètres de configuration de l'algorithme
        self.population = []                # Liste des individus de la population
        self.population_selection = []    # Liste des individus de l'selection
        self.new_population=[]              # Liste pour la nouvelle population générée
        self.inputs=[]                      # Données d'entrée pour l'évaluation de la fitness
        self.outputs=[]                     # Valeurs cibles pour l'évaluation de la fitness
        self.widget=None                    # Important : fait office de pointeur entre les calculs effectués et l'interface graphique
        self.isRunning=False                # Indicateur de l'état de l'exécution de l'algorithme
        self.elapsed_time=0                 # Temps écoulé depuis le démarrage
        self.stop=False
        self.min_val=0
        self.max_val=0

    def initialise(self,config,inputs,outputs,widget):
        """
        Configure les paramètres de l'algorithme.
        Args:
            config (obj): classe de configuration.
            inputs (list): Données d'entrée.
            outputs (list): Valeurs de la fonction pour les inputs.
            widget (object): Interface graphique associée.
        """
        # Initialisation des attributs à partir des paramètres de configuration
        self.population = []
        self.inputs=inputs
        self.outputs=self._normalise(outputs)
        self.widget=widget
        self.config=config
        self.stop=False

        GeneGP.init_fonctions(config)
        # Initialisation des générateurs aléatoires avec une graine si spécifiée
        if self.config.seed!=0 :
            random.seed(self.config.seed)
            np.random.seed(self.config.seed)
        # Ajustement de la taille de l'échantillon en fonction de la population
        if self.config.size_echantillon>self.config.size_population:
            self.config.size_echantillon=self.config.size_population




    def execute(self):
        """
        Lance l'exécution de l'algorithme génétique, comprenant les étapes de sélection,
        reproduction, mutation et remplacement des individus.
        """
        self.population   = []              # Réinitialisation de la population


        self.stop=False
        self.isRunning=True                 # Indicateur que l'algorithme est en cours
        start_time=time.time()              # Démarrage du chronomètre
        self.elapsed_time=0

        self.populate()                     # Initialisation de la population

        curent_fitness=sys.float_info.max   # Valeur initiale très élevée pour la fitness
        iteration=0  
        # Boucle principale de l'algorithme avec critères d'arrêt
        while( iteration<self.config.max_iterations   
                and  curent_fitness>=self.config.seuil_fitness  
                and self.elapsed_time<=self.config.duree_maximum  
                and not self.isStop()):

            self.setAvancement("itération",iteration,self.config.max_iterations) #pour la jauge
            #self.populate_liste()
            self.iterate(iteration)                      # Exécution d'une itération
            best= self.get_best()                        # Récupération du meilleur individu
            if best is not None:
                curent_fitness= best.fitness                 # Mise à jour de la fitness
                self.elapsed_time = time.time() - start_time # Mise à jour du temps écoulé              # Sauvegarde des meilleurs résultats
                self.affiche_chromosome(iteration,best)         #pour le graphe
                if self.config.verbose :
                    print(iteration,curent_fitness,best.generation,"[",best.formule,"]")
            iteration+=1


        self.affiche_resultats()                         # Affichage des résultats finaux
        self.isRunning=False                             # L'algorithme s'est terminé


    def populate(self):
        """
        Initialise la population 
        """
        if self.config.fichier_populate!="" :
            self.populate_read(self.config.fichier_populate)
        else:
            self.populate_generate()


    def iterate(self,iteration):
        """
        Gère l'évolution d'une génération : sélection, croisement et mutation.
        """

        self.new_population=[]                   # Liste pour la nouvelle génération

        self.population_selection=self.selection()       # Sélection des individus pour cette génération
        size=len(self.population_selection)
 
        i=0
        while i <size//2:
            mother,father=self.mariage(i, size)
            # Croisement pour produire deux enfants
            #print(f"mariage {i} : mother - {mother.fitness}={mother.formule} father - {father.fitness}={father.formule}")
            child1,child2  = self.croisement(mother, father)
            child1=self.mutate(child1)   
            if child1 is not None and not self.inPopulate(child1.formule):
                child1.generation=iteration
                self.new_population.append(child1)              # Ajout à la nouvelle population
                #print(f"child1={child1.formule} fitness={child1.fitness}")
            child2=self.mutate(child2)   
            if child2 is not None and not self.inPopulate(child2.formule):
                child2.generation=iteration
                self.new_population.append(child2)  
                #print(f"child2={child2.formule} fitness={child2.fitness}")
            i+=1
        # Mise à jour de la population actuelle
        self.remplacement()

    def selection(self):
        """
        Sélectionne un sous-ensemble d'individus pour la reproduction.
        """
  
        if  self.config.mode_selection==self.config.SELECTION_BEST:
            self.population.sort(reverse=False,key=lambda x:x.fitness)                      # Tri de population par fitness croissante
            selection=self.population[0:self.config.size_echantillon]              # Échantillonnage des best
        elif  self.config.mode_selection==self.config.SELECTION_WORST:
            self.population.sort(reverse=True,key=lambda x:x.fitness)                       # Tri de population par fitness decroissante
            selection=self.population[0:self.config.size_echantillon]              # Échantillonnage des worst
        else: #self.config.mode_selection==self.config.SELECTION_RANDOM:
            selection=random.sample(self.population, self.config.size_echantillon) # Échantillonnage aléatoire

        selection.sort(reverse=False,key=lambda x:x.fitness)                       # Tri des individus par fitness 
        return selection

    def mariage(self,pos, size):
        """
        sélection d'un couple de deux chromosomes.
        """
 
        if  self.config.mode_mariage==self.config.MARIAGE_BEST:
            mother = self.population_selection[2*pos]
            father = self.population_selection[2*pos+1]
        elif  self.config.mode_mariage==self.config.MARIAGE_EXTREME:
            mother = self.population_selection[pos]
            father = self.population_selection[size-pos-1]
        else: # self.config.mode_mariage==self.config.MARIAGE_RAND:
            mother = self.population_selection[np.random.randint(size)]
            father = self.population_selection[np.random.randint(size)]
        return mother,father

    def croisement(self,mother, father):
        """
        croisement de deux chromosommes (mother, father).
        """
        # Créer de nouveaux enfanst en croisant les gènes des deux chromosomes (mère et père)
        if  self.config.mode_croisement==self.config.CROISEMENT_MIDDLE:
            return ChromosomeGP.croisement_middle(mother, father)
        elif  self.config.mode_croisement==self.config.CROISEMENT_ABSORPTION_PARTIELLE :
            return ChromosomeGP.croisement_absorption_partielle(mother, father)
        else  :# self.config.mode_croisement==self.config.CROISEMENT_ABSORPTION_TOTALE :
            return ChromosomeGP.croisement_absorption_totale(mother, father)
  
    def mutate(self,child):
        """
        Ajoute un enfant à la nouvelle population, avec éventuellement une mutation.
        """
        if child is None :
            return None
        tolerence=random.random()
        depth=child.depth
        # Vérification de la profondeur maximale
        if depth > self.config.max_depth :
            if tolerence < self.config.tolerance_gene_Length:
                return None

        if tolerence > self.config.tolerance_gene_Mutate:
            if  self.config.mode_mutation==self.config.MUTATION_DEPLACE:
                child.mutate_deplace () 
            elif  self.config.mode_mutation==self.config.MUTATION_SWAP:
                child.mutate_swap() 
            else  :# self.config.mode_mutation==self.config.MUTATION_REPLACE :
                child.mutate_remplace() 

        child.calculate_fitness(self.inputs, self.outputs,self.min_val,self.max_val) # Calcul de la fitness
        if not child.isFitnessValide():                    # Si l'enfant est non valide
                return None
        return  child      

    def remplacement(self):
        """
        remplacement un sous-ensemble d'individus pour la reproduction.
        """

        if  self.config.mode_remplacement == self.config.REMPLACEMENT_CHILD_ONLY:
            self.population=self.new_population.copy()                                      # remplacer la population par les enfants 
        elif  self.config.mode_remplacement == self.config.REMPLACEMENT_CHILD_ADD:
            self.population+=self.new_population                                            # ajouter les enfants  à la population 
        elif  self.config.mode_remplacement == self.config.REMPLACEMENT_MIXT_RAND:
            self.population+=self.new_population
            self.population=random.sample(self.population, self.config.size_population)     # Limitation à la taille de la population
        else:#  self.config.mode_remplacement == self.config.REMPLACEMENT_MIXT_BEST:
            self.population+=self.new_population                                            # mixer parents et enfants
            self.population.sort(reverse=False,key=lambda x:x.fitness)                      # Tri par fitness
            self.population=self.population[0:self.config.size_population]                  # Limitation à la taille de la population
 
        self.config.size_population=len(self.population)
        if self.config.size_echantillon>self.config.size_population:
            self.config.size_echantillon=self.config.size_population
        
        
 


#------------------------------------------------------------------------
    def _newChromosome(self,line:str=None):
        """
        Crée un nouveau chromosome aléatoire.
        """
        if line is not None:
            newitem=ChromosomeGP(self.config, 'none')
            newitem.read_gene(line)
            newitem.calculate_fitness(self.inputs, self.outputs,self.min_val,self.max_val)
        else:
            newitem=ChromosomeGP(self.config,  'rand')
            # Regénération des individus jusqu'à obtenir une fitness valide
            while not newitem.isFitnessValide() :
                newitem.initialise_Item("rand")
                newitem.calculate_fitness(self.inputs, self.outputs,self.min_val,self.max_val) 
                if self.isStop():
                    return None
        return newitem

    def _newAffineChromosome(self):
        """
        Initialise un chromosome affine passant par le premier et dernier point de donnée.
        """
        if len(self.inputs) < 2 or len(self.outputs) < 2:
            return None

        x1 = self.inputs[0]
        y1 = self.outputs[0]
        xn = self.inputs[-1]
        yn = self.outputs[-1]
        if xn == x1:
            return None

        # Calcul de la droite y = a*x + b
        a = (yn - y1) / (xn - x1)
        b = y1 - a * x1

        # Construire une formule linéaire simple : (+ (* a x) b)
        # Ne pas oublier que les constantes doivent être entières dans le modèle actuel.
        # On arrondit a et b pour l'initialisation.
        a_int = int(round(a))
        b_int = int(round(b))

        chrom = ChromosomeGP(self.config, 'none')
        chrom.gen = [
            GeneGP.create_gene(GeneGP.TYPE_GEN_FONCTION_BINAIRE, '+'),
            GeneGP.create_gene(GeneGP.TYPE_GEN_FONCTION_BINAIRE, '*'),
            GeneGP.create_gene(GeneGP.TYPE_GEN_TERMINAL_INTEGER, a_int),
            GeneGP.create_gene(GeneGP.TYPE_GEN_TERMINAL_SYMBOLE, 'x'),
            GeneGP.create_gene(GeneGP.TYPE_GEN_TERMINAL_INTEGER, b_int)
        ]
        chrom.set_variables()
        chrom.calculate_fitness(self.inputs, self.outputs,self.min_val,self.max_val)
        if chrom.isFitnessValide():
            return chrom
        return None
    
    def populate_liste(self):
        """
        Initialise la population en créant des individus jusqu'à atteindre la taille spécifiée.
        """
        #if not self.config.verbose :
        #        return
        print("Population actuelle :")
        i=0    
        for item in self.population:
            i+=1
            if (item is not None):
                print(f"item {i} : {item.formule}")
    
    def populate_generate(self):
        """
        Initialise la population en créant des individus jusqu'à atteindre la taille spécifiée.
        """
        newitem=self._newAffineChromosome() or self._newChromosome() # Création d'un premier individu de base
        if (newitem is not None):
            self.setAvancement(f"Création de populations  {newitem.formule}",1,self.config.size_population)
            self.population.append(newitem)
        i=2            
        while i <= self.config.size_population:
            if self.isStop():
                break
            newitem=self._newChromosome()
            if (newitem is not None):
                if not self.inPopulate(newitem.formule):
                    self.population.append(newitem)
                    self.setAvancement(f"Création de populations  {newitem.formule}",i,self.config.size_population) # Mise à jour de l'interface graphique
                    if self.config.verbose :
                        print(i,newitem.fitness)
                    i+=1
                    
                    

    def populate_read(self,fichier):
        """
        Initialise la population en chargeant des individus à partir d'un fichier.
        """
        self.population=[] # Vide la population existante
        i=0
        with open(fichier, 'r') as file:
            line_list = file.readlines(); # Lecture du fichier 
        for line in line_list:
            line=line.strip()
            if line=="" :continue
            if self.config.verbose :
                print(i,line)
            newitem=ChromosomeGP(self.config, 'none')
            newitem.read_gene(line)
            newitem.calculate_fitness(self.inputs, self.outputs,self.min_val,self.max_val)
            if newitem.isFitnessValide():
                self.population.append(newitem) # Ajout des individus valides à la population
            i+=1
        # Ajustement de la taille de l'échantillon en fonction de la population
        self.config.size_population=len(self.population)
        if self.config.size_echantillon>self.config.size_population:
            self.config.size_echantillon=self.config.size_population

    def populate_write(self, fichier):
        """
        Écrire la population dans un fichier.
        """
        strOut=""
        for item in self.population:
            strOut+=item.write_gene()# Conversion des génomes en chaîne de caractères
            strOut+="\n"
        with open(fichier, 'w') as file:
            file.write(strOut);       
    
    def inPopulate(self, formule):    
        for item in self.population:
            if item.formule==formule:
                return True
        return False
#------------------------------------------------------------------------

    def isStop(self):
        """
        Vérifie si l'algorithme doit s'arrêter.
        """
        return  self.stop

    def setStop(self):
        """
        Vérifie si l'algorithme doit s'arrêter.
        """
        self.stop=True

    def setAvancement(self,str_message,pos_value,max_value):
        """
        Met à jour l'interface graphique avec l'état d'avancement.
        """
        if self.widget is not None:
            self.widget.set_jauge_value(str_message,pos_value,max_value)

    def affiche_resultats(self):
        """
        Affiche les résultats finaux de l'algorithme.
        """
        if self.widget is not None:
            self.widget.affiche_resultats( self.inputs, self.outputs,self.min_val,self.max_val,self.config.startValue,self.config.horizon)

    def affiche_chromosome(self,iteration,chromosome):
        """
        Met à jour l'interface graphique avec le  chromosome.
        """
        if self.widget is not None:
            try:
                # transmettre les entrées et le temps écoulé au widget pour qu'il puisse calculer y_pred et afficher le temps
                
                self.widget.affiche_chromosome(iteration, chromosome, self.inputs, self.elapsed_time,self.min_val,self.max_val)
            except TypeError:
                # compatibilité si le widget n'accepte pas le paramètre inputs
                self.widget.affiche_chromosome(iteration, chromosome)

    def get_best(self):
        """
        Récupère le meilleur individu de la population.
        """
        if len(self.population) ==0:
            return None
        self.population.sort(reverse=False,key=lambda x:x.fitness)
        return self.population[0]

    def _normalise(self,outputs):
        """
        Normalise les valeurs de sortie pour qu'elles soient comprises entre 0 et 1.
        """
        if len(outputs)==0:
            return outputs
        self.min_val=min(outputs)
        self.max_val=max(outputs)
        ecart_val= self.max_val- self.min_val
        if ecart_val==0:
            return [0.5 for _ in outputs]  # Si toutes les valeurs sont identiques, renvoyer 0.5

        return [(y -  self.min_val) / ecart_val for y in outputs]

    def _denormalise(self,normalized_outputs):
        """
        Restaure les valeurs normalisées à leur échelle d'origine.
        """
        return [y * (self.max_val - self.min_val) + self.min_val for y in normalized_outputs]   
    