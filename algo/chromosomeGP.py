import numpy as np
import random
import math
from sympy import symbols, simplify
from algo.geneGP import GeneGP
"""
ChromosomeGP:
Cette classe représente un individu génétique sous forme de chromosome dans un algorithme de programmation génétique (GP), et elle contient des méthodes pour gérer la création, l'évaluation, la mutation, et le croisement des chromosomes.

Attributs
	genes : Liste des gènes du chromosome, où chaque gène peut être une fonction ou un terminal.
	fitness : La valeur de fitness du chromosome, qui évalue sa performance par rapport à une solution optimale.
	max_genes : Le nombre maximal de gènes dans le chromosome, ce qui détermine la "taille" du chromosome.
Méthodes principales
	initialise_chromosome : Initialise le chromosome en fonction de la méthode spécifiée (full, grow, etc.).
	full : Crée un chromosome complet, où tous les gènes sont remplis de fonctions ou de terminaux.
	grow : Crée un chromosome en mélangeant des fonctions et des terminaux, avec une probabilité plus élevée de choisir des terminaux.
	calculate_fitness : Calcule la fitness du chromosome en comparant ses sorties avec les sorties attendues pour un ensemble d'entrées.
	mutate : Applique une mutation sur un gène aléatoire du chromosome, modifiant ainsi sa structure génétique.
	cross_over : Applique un croisement entre ce chromosome et un autre (le père), générant un nouvel enfant avec les gènes des deux parents.
	evaluate : Évalue le chromosome pour une donnée d'entrée en calculant le résultat de chaque gène.
""" 

class ChromosomeGP():
    """
    Classe représentant un individu génétique sous forme de chromosome dans un algorithme de programmation génétique.
    Cette classe hérite de `ItemGP` et implémente les méthodes spécifiques pour manipuler des chromosomes.
    
    Attributs :
        genes (list): Liste représentant les gènes du chromosome. Chaque gène peut être une fonction ou un terminal.
        fitness (float): La valeur de fitness de l'individu, indiquant sa performance par rapport à la solution optimale.
        depth : La profondeur   de l'individu. Cela détermine la "taille" ou la complexité maximale de l'individu dans l'algorithme génétique.
        config : Instance de la boite de configuration.
        fitness : La valeur de fitness de l'individu, représentant sa performance ou son adéquation avec la solution optimale. Initialisée à NaN jusqu'à ce qu'elle soit calculée.
    """
    def __init__(self, config, method='full'):
        """
        Initialise un chromosome génétique avec une profondeur donnée, une méthode d'initialisation et un nombre maximal de gènes.

        Args:
            config (obj): Instance de la boite de config.
            depth (int): Profondeur maximale de l'arbre ou du chromosome.
            method (str): Méthode d'initialisation du chromosome ('full', 'grow', etc.).
        """
        self.generation=0            # indice de génération
        self.gen = []                # Liste des gènes du chromosome.
        self._depth = 0              # Profondeur de l'individu.
        self.formule=""              # équation au format texte
        self.config = config           # Instance de la boite à outils génétique.
        self.fitness = float('nan')  # Initialisation de la fitness à NaN (indique qu'il n'a pas encore été évalué).
        self.initialise_Item(method) # Initialisation de l'individu avec la méthode spécifiée.

#-----------------------------------------------------------------------------

    def initialise_Item(self, method):
        """
        Initialise l'individu génétique en fonction de la méthode spécifiée.

        Args:
            method (str): Méthode d'initialisation de l'individu ('none', 'full', 'grow', etc.).
        """
        self.gen = []  # Initialise les éléments de base de l'individu.
        if method == 'none':
            return  # Si aucune méthode, rien n'est fait.
        elif method == 'full':
            self.full()  # Crée l'individu avec la méthode 'full'.
        elif method == 'grow':
            self.grow()  # Crée l'individu avec la méthode 'grow'.
        else:
            # Si aucune méthode explicite, choisit aléatoirement entre 'full' et 'grow'.
            if random.random() > 0.5:
                self.grow()
            else:
                self.full()
        self.set_variables()

    def full(self, level = 0):
        """
        Crée un chromosome complet, c'est-à-dire un chromosome où tous les gènes sont des fonctions ou des terminaux
        jusqu'à la profondeur maximale spécifiée.

        Cette méthode construit un chromosome dont chaque gène est un élément complet, en remplissant l'arbre génétique
        avec des fonctions et des terminaux jusqu'à la profondeur maximale.

        Retourne:
            None
        """
        if level == self.config.max_depth:
            self.gen.append(GeneGP.random_choice_terminal())
        else:
            elem = GeneGP.random_choice_fonction() #pour pouvoir choisir aleéatoirement dans toutes les fonctions unaires et binaires
            if elem.is_fonction_binaire():
                self.gen.append(elem)
                self.full(level + 1)
                self.full(level + 1) # une fois à droite et une fois à gauche (car fct binaire)
            else: #fonction unaire
                self.gen.append(elem)
                self.full(level + 1)
        
    def grow(self, level = 0):
        """
        Crée un chromosome en utilisant la méthode 'grow', qui consiste à mélanger des fonctions et des terminaux
        tout en ayant une probabilité plus élevée de sélectionner des terminaux à des niveaux plus profonds.

        Cette méthode génère un chromosome où certains gènes peuvent être des fonctions et d'autres des terminaux.
        Le nombre de terminaux augmente à mesure que l'on descend dans l'arbre.

        Retourne:
            None
        """
        if level == self.config.max_depth:
            self.gen.append(GeneGP.random_choice_terminal())
        else:
            if random.random() < 0.5:
                elem = GeneGP.random_choice_fonction()
                if elem.is_fonction_binaire():
                    self.gen.append(elem)
                    self.grow(level + 1)
                    self.grow(level + 1)
                else:
                    self.gen.append(elem)
                    self.grow(level + 1)
            else:
                elem = GeneGP.random_choice_terminal()
                self.gen.append(elem)
#-----------------------------------------------------------------------------
    def isFitnessValide(self):
        """
        Vérifie si la fitness de l'individu est valide (c'est-à-dire non NaN et non infinie).
        
        Returns:
            bool: True si la fitness est valide, False sinon.
        """
        return not math.isnan(self.fitness) and not math.isinf(self.fitness)


    def calculate_fitness(self, inputs, outputs, min_val=None, max_val=None):
        """
        Calcule la fitness de l'individu en fonction des entrées et sorties fournies.

        Args:
            inputs (list): Liste des entrées à utiliser pour l'évaluation.
            outputs (list): Liste des sorties attendues pour chaque entrée.

        Returns:
            float: La fitness calculée de l'individu.
        """
        diff = 0  # Variable pour accumuler les différences quadratiques.
 
        # Calcule la différence entre la sortie attendue et la sortie générée pour chaque entrée.
        try:
            for i in range(len(inputs)):

                eval_in = self.evaluate(inputs[i])  # Évalue l'individu pour une entrée donnée : cf ChromosomeGP
                val_out = outputs[i]  # Valeur attendue pour cette entrée.
                if min_val is not None and max_val is not None:
                    # Normalisation de la formule   
                    ecart_val= max_val- min_val
                    if ecart_val==0:
                        ecart_val=1
                    eval_in = ecart_val*eval_in+min_val
                    val_out = ecart_val*val_out+min_val

                ecart = eval_in - val_out  # Écart entre la sortie et la valeur attendue.
                diff += ecart ** 2  # Ajoute le carré de l'écart à la différence totale.

            # Calcule la moyenne des différences quadratiques et renvoie la fitness.
            self.fitness= np.sqrt(diff) / len(inputs)
            return self.fitness


        except Exception as ex:
            # Si une exception se produit lors de l'évaluation, marque la fitness comme NaN.
            return float('nan')

    def evaluate(self, input):
        """
        Évalue le chromosome pour une donnée d'entrée spécifique.
        Args:
            input (float): Valeur d'entrée.
        Retourne:
            float: Résultat de l'évaluation.
        """
        return self.__evaluate(input,0)[0]
        
    def __evaluate(self, input, position = 0): #fct auxiliaire 
        elem=self.gen[position]
        if elem.is_terminal(): 
            return elem.evaluate(input), position + 1  
        elif elem.is_fonction_binaire():
            left, position = self.__evaluate(input, position + 1)
            right, position = self.__evaluate(input, position)
            return elem.evaluate(left,right), position
        else:
            left, position = self.__evaluate(input, position + 1)
            return elem.evaluate(left), position

#-----------------------------------------------------------------------------

    def croisement_middle(mother, father):
        """
        Réalise le croisement entre le chromosome actuel (mère) et un chromosome père.
        Args:
            father (Chromosome): Chromosome père.
        Returns:
            Chromosome: Nouveau chromosome issu du croisement.
        """
        len_mother= len(mother.gen)
        len_father= len(father.gen)
        max_depth=2*mother.config.max_depth

        child1 = ChromosomeGP(mother.config, 'none')
        child2 = ChromosomeGP(father.config,  'none')
        start_m = np.random.randint( len_mother)#choix aléatoire de la position dans le tableau du chromosome mère 
        end_m   = mother.position_fin_branche(start_m )#fin de la branche issue de la position start_m dans le tableau du chromosome mere 
        start_f = np.random.randint( len_father)#choix aléatoire de la position dans le tableau du chromosome père 
        end_f   = father.position_fin_branche(start_f) #fin de la branche issue de la position start_f dans le tableau du chromosome père 
        child1.gen = mother.gen[:start_m] + father.gen[start_f : end_f] + mother.gen[end_m :]# Affecte les gènes croisés à l'enfant 1
        child2.gen = father.gen[:start_f] + mother.gen[start_m : end_m] + father.gen[end_f :]# Affecte les gènes croisés à l'enfant 2
        child1.set_variables()
        child2.set_variables()
        if(child1.depth>max_depth):
            child1=None
        if(child2.depth>max_depth):
            child2=None
        return child1,child2

    def croisement_absorption_partielle(mother, father):
        """
        Réalise le croisement entre le chromosome actuel (mère) et un chromosome père.
        Args:
            father (Chromosome): Chromosome père.
        Returns:
            Chromosome: Nouveau chromosome issu du croisement.
        """
        len_mother= len(mother.gen)
        len_father= len(father.gen)

        child1 = ChromosomeGP(mother.config, 'none')
        child2 = ChromosomeGP(father.config,  'none')
        start_m = np.random.randint( len_mother)#choix aléatoire de la position dans le tableau du chromosome mère 
        end_m   = mother.position_fin_branche(start_m )#fin de la branche issue de la position start_m dans le tableau du chromosome mere 
        start_f = np.random.randint( len_father)#choix aléatoire de la position dans le tableau du chromosome père 
        end_f   = father.position_fin_branche(start_f) #fin de la branche issue de la position start_f dans le tableau du chromosome père 
        child1.gen = mother.gen[:start_m]+ father.gen[:start_f]+mother.gen[start_m : end_m]+father.gen[end_f :]+ mother.gen[end_m :] 
        child2.gen = father.gen[:start_f]+ mother.gen[:start_m]+father.gen[start_f : end_f]+mother.gen[end_m :]+ father.gen[end_f :]
        child1.set_variables()
        child2.set_variables()
        return child1,child2

    def croisement_absorption_totale(mother, father):
        """
        Réalise le croisement entre le chromosome actuel (mère) et un chromosome père.
        Args:
            father (Chromosome): Chromosome père.
        Returns:
            Chromosome: Nouveau chromosome issu du croisement.
        """
        len_mother= len(mother.gen)
        len_father= len(father.gen)

        child1 = ChromosomeGP(mother.config, 'none')
        child2 = ChromosomeGP(father.config,  'none')
        start_m = np.random.randint( len_mother)#choix aléatoire de la position dans le tableau du chromosome mère 
        end_m   = mother.position_fin_branche(start_m )#fin de la branche issue de la position start_m dans le tableau du chromosome mere 
        start_f = np.random.randint( len_father)#choix aléatoire de la position dans le tableau du chromosome père 
        end_f   = father.position_fin_branche(start_f) #fin de la branche issue de la position start_f dans le tableau du chromosome père 
        child1.gen = mother.gen[:start_m] + father.gen + mother.gen[end_m :]# Affecte les gènes croisés à l'enfant 1
        child2.gen = father.gen[:start_f] + mother.gen + father.gen[end_f :]# Affecte les gènes croisés à l'enfant 2
        child1.set_variables()
        child2.set_variables()
        return child1,child2

#------------------------------------------------------------------------
    def mutate_remplace(self):
        """
        Applique une mutation sur un gène aléatoire du chromosome.
        """
        
        position = np.random.randint(len(self.gen))

        element=self.gen[position]
        oldFormule=self.formule

        if element.is_fonction():
            if  element.is_fonction_unaire():
                newGen = GeneGP.random_choice_fonction_unaire()
            else:
                newGen = GeneGP.random_choice_fonction_binaire()
        else:
            newGen = GeneGP.random_choice_terminal()

        self.gen[position]=newGen
        self.set_variables()

        #print (f"mutation remplace position={position}  {element.name_gen} par {newGen.name_gen} : {oldFormule} par {self.formule} ")
  
    def mutate_swap(self):
        """
        Applique une mutation d'échange de la position de deux gènes du chromosome de façon  aléatoire .
        """
        if len(self.gen)<=3:
            return
        start_1 = np.random.randint(1,len(self.gen))
        end_1   = self.position_fin_branche(start_1 )#fin de la branche issue de la position start_1 dans le tableau du chromosome   
        start_2 = np.random.randint(1,len(self.gen))
        end_2   = self.position_fin_branche(start_2 )#fin de la branche issue de la position start_2 dans le tableau du chromosome 

        #if self.gen[start_1].type_gen!=self.gen[start_2].type_gen:
        #    return

        if (start_1<=start_2 and start_2<=end_1) or (start_2<=start_1 and start_1<=end_2):
            #print ("aucun traitement")
            return
        if start_1 < start_2 :
            self.gen = self.gen[:start_1] + self.gen[start_2 : end_2] + self.gen[end_1 :start_2] + self.gen[start_1 : end_1] + self.gen[end_2 :]
        else:
            self.gen = self.gen[:start_2] + self.gen[start_1 : end_1] + self.gen[end_2 :start_1] + self.gen[start_2 : end_2] + self.gen[end_1 :]
        self.set_variables()
   
    def mutate_deplace(self):
        """
        Applique une mutation sur un gène aléatoire du chromosome en déplaçant sa position.
        """
        if len(self.gen)<=2:
            return
        start_1 = np.random.randint(1,len(self.gen))
        end_1   = self.position_fin_branche(start_1 )#fin de la branche issue de la position start_1 dans le tableau du chromosome   

        max_iteration=10
        cpt=0
        while  cpt<max_iteration:
            pos_cible = np.random.randint(len(self.gen))
            element=self.gen[pos_cible]
            if (start_1>pos_cible or pos_cible>end_1) :
                if  element.is_terminal()  :
                    break
            cpt+=1
        if cpt==max_iteration:
            return

        #print(start_1,end_1,self.gen[start_1 : end_1],pos_cible,element)

        nullElement=[GeneGP.create_gene(GeneGP.TYPE_GEN_TERMINAL_INTEGER,0)]
        if start_1 > pos_cible :
            self.gen = self.gen[:pos_cible] + self.gen[start_1 : end_1] + self.gen[pos_cible+1 :start_1]+ nullElement+ self.gen[end_1 :]
        else:
            self.gen = self.gen[:start_1] +nullElement+ self.gen[end_1 :pos_cible] + self.gen[start_1 : end_1] + self.gen[pos_cible+1 :]

        self.set_variables()

#------------------------------------------------------------------------
    def read_gene(self,str_line):
        """
        Lit un gène depuis une chaîne de caractères.
        Args:
            str_line (str): La ligne représentant le gène.
        Returns:
            list: Liste de valeurs représentant le gène.
        """
        self.gen=[]
        items=str_line.split(';')
        for item in items:
            valeur,type_val=item.split(':')
            elem=GeneGP.read_str(int(type_val),valeur)
            self.gen.append(elem)

    def simplify(self):
        try:
            formule=self.simplifyFormule()
            if formule != self.formule:
                self._read_formule(formule)
        except Exception as e:
            print(f"Erreur lors de la simplification de l'expression: {formule}")

    def simplifyFormule(self):
        try:
            x = symbols('x')
            simp_formule = str(simplify(self.formule))  
            return simp_formule
        except Exception as e:
            print(f"Erreur lors de la simplification de l'expression: {self.formule}")
            return self.formule

    def write_gene(self):
        """
        Écrit un gène sous forme de chaîne de caractères.
        Args:
            gen (list): Le gène sous forme de liste.
        Returns:
            str: La chaîne de caractères représentant le gène.
        """
        strOut=""
        for item in self.gen:
           if strOut!="" : strOut+=";"
           strOut+= item.write_str() 
        return strOut
#------------------------------------------------------------------------
    def set_variables(self):
        """
        Méthode auxiliaire pour calculer la profondeur.
         Returns:
           int: profondeur.
        """        
        self.depth   = self.__get_depth_aux()[0] - 1
        self.formule = self.__formule_aux(0)[1]

    def trace(self):
        strOut=""
        for item in self.gen:
           if strOut!="" : strOut+=" "
           strOut+= item.name_gen 
        print(strOut)
    def denormalise(self,min_val=None, max_val=None):
        """
        Méthode pour dénormaliser la formule du chromosome en utilisant les valeurs min et max fournies.
        Args:
            min_val (float): La valeur minimale utilisée pour la normalisation.
            max_val (float): La valeur maximale utilisée pour la normalisation.
        """
        if min_val is not None and max_val is not None:
            ecart_val = max_val - min_val
            if ecart_val == 0:
                ecart_val = 1
            self.formule = str(ecart_val) + '*(' + self.formule + ') +' + str(min_val)  

#------------------------------------------------------------------------
    def position_fin_branche(self,position):
        """
        parcourt le tableau de genes jusqu'a la fin de l'arbre.
        Args:
            position (int): position courante dans le tableau de gen.
        Returns:
             position de la fin de l'arbre.
        """
        if self.gen[position].is_terminal () :
            return position + 1
        elif self.gen[position].is_fonction_unaire ():
            return self.position_fin_branche(position + 1)
        else:
            new_position = self.position_fin_branche(position + 1)
            return self.position_fin_branche(new_position)
#------------------------------------------------------------------------

    def __get_depth_aux(self, position = 0):
        """
        Méthode auxiliaire pour calculer la profondeur.
        Args:
            position (int): position courante dans le tableau de gen.
        Returns:
            int: position courante.
            int: profondeur.
        """        
        elem = self.gen[position]
        
        if elem.is_fonction_binaire():
            left, position = self.__get_depth_aux(position + 1)
            right, position = self.__get_depth_aux(position)

            return 1 + max(left, right), position
        elif elem.is_fonction_unaire():
            left, position = self.__get_depth_aux(position + 1)
            return left + 1, position
        else:
            return 1, position + 1
#------------------------------------------------------------------------
 
    def __formule_aux(self, position ):
        """
        Méthode auxiliaire pour générer la formule lisible.
        Args:
            position (int): position courante dans le tableau de gen.
        Returns:
           str: formules au format texte
        """        
        elem=self.gen[position]        
        if elem.is_terminal(): 
            return position + 1, elem.writeStr()
        elif elem.is_fonction_binaire():
            position, str_next1 = self.__formule_aux(position + 1)
            position, str_next2 = self.__formule_aux(position)
            return position, elem.writeStr(str_next1,str_next2)
        elif elem.is_fonction_unaire():
            position, str_next = self.__formule_aux(position + 1)
            return position, elem.writeStr(str_next)



    def _read_formule(self,formule):
        """
        Parse une formule mathématique (chaîne) et construit le tableau de gènes `self.gen`.
        La représentation interne est en préfixe : racine, sous-arbre gauche, sous-arbre droit.
        Supporte : variables (`x`), entiers, fonctions unaires (sin,cos,ln,...), opérateurs binaires (+, -, *, /, **).
        """
        s = str(formule)
        # Tokenisation simple
        tok = []
        i = 0
        while i < len(s):
            c = s[i]
            if c.isspace():
                i += 1
                continue
            # nombre entier (avec signe si approprié)
            if (c == '-' and (i == 0 or s[i-1] in '(+-*/')) or c.isdigit():
                j = i
                if s[j] == '-':
                    j += 1
                while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                    j += 1
                num_str = s[i:j]
                try:
                    if '.' in num_str:
                        val = float(num_str)
                    else:
                        val = int(num_str)
                except:
                    val = 0
                tok.append(('NUM', val))
                i = j
                continue
            # double étoile
            if c == '*' and i + 1 < len(s) and s[i+1] == '*':
                tok.append(('OP', '**'))
                i += 2
                continue
            # opérateurs simples et parenthèses
            if c in '+-*/()':
                tok.append(('OP', c))
                i += 1
                continue
            # identifiant (fonction ou variable)
            if c.isalpha():
                j = i + 1
                while j < len(s) and (s[j].isalpha()):
                    j += 1
                ident = s[i:j]
                tok.append(('ID', ident))
                i = j
                continue
            # tout le reste : ignorer
            i += 1

        # analyseur récursif (precedence)
        idx = 0
        def peek():
            return tok[idx] if idx < len(tok) else (None, None)
        def advance():
            nonlocal idx
            idx += 1
            return tok[idx-1] if idx-1 < len(tok) else (None, None)

        def parse_expression():
            node = parse_term()
            while True:
                t = peek()
                if t[0] == 'OP' and t[1] in ('+', '-'):
                    op = advance()[1]
                    right = parse_term()
                    node = ('bin', op, node, right)
                else:
                    break
            return node

        def parse_term():
            node = parse_power()
            while True:
                t = peek()
                if t[0] == 'OP' and t[1] in ('*', '/'):
                    op = advance()[1]
                    right = parse_power()
                    node = ('bin', op, node, right)
                else:
                    break
            return node

        def parse_power():
            node = parse_factor()
            t = peek()
            if t[0] == 'OP' and t[1] == '**':
                advance()
                right = parse_power()
                node = ('bin', '**', node, right)
            return node

        def parse_factor():
            t = peek()
            if t[0] == 'NUM':
                val = advance()[1]
                return ('num', val)
            if t[0] == 'ID':
                idtok = advance()[1]
                # fonction si parenthèse suit
                nxt = peek()
                if nxt[0] == 'OP' and nxt[1] == '(':
                    advance()  # consomme '('
                    child = parse_expression()
                    # consommer ')'
                    if peek()[0] == 'OP' and peek()[1] == ')':
                        advance()
                    return ('func', idtok, child)
                else:
                    return ('var', idtok)
            if t[0] == 'OP' and t[1] == '(':
                advance()
                node = parse_expression()
                if peek()[0] == 'OP' and peek()[1] == ')':
                    advance()
                return node
            # gestion du unaire '-' devant une expression
            if t[0] == 'OP' and t[1] == '-':
                advance()
                node = parse_factor()
                return ('bin', '-', ('num', 0), node)
            return ('num', 0)

        try:
            ast = parse_expression()
        except Exception:
            ast = ('num', 0)

        # conversion AST -> préfix list de gènes
        new_gen = []
        def emit(node):
            if node[0] == 'num':
                # arrondir aux entiers si possible
                v = node[1]
                try:
                    iv = int(round(float(v)))
                except:
                    iv = 0
                new_gen.append(GeneGP.create_gene(GeneGP.TYPE_GEN_TERMINAL_INTEGER, iv))
            elif node[0] == 'var':
                name = node[1]
                new_gen.append(GeneGP.create_gene(GeneGP.TYPE_GEN_TERMINAL_SYMBOLE, name))
            elif node[0] == 'func':
                fname = node[1]
                # normalisation: exp -> e
                if fname == 'exp':
                    fname = 'e'
                new_gen.append(GeneGP.create_gene(GeneGP.TYPE_GEN_FONCTION_UNAIRE, fname))
                emit(node[2])
            elif node[0] == 'bin':
                op = node[1]
                # normaliser '**' vs '^'
                new_gen.append(GeneGP.create_gene(GeneGP.TYPE_GEN_FONCTION_BINAIRE, op))
                emit(node[2])
                emit(node[3])

        emit(ast)
        self.gen = new_gen
        try:
            self.set_variables()
        except Exception:
            # si set_variables échoue, on laisse self.gen défini
            pass

