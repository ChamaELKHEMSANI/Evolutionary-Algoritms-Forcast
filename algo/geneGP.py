import sys
import random


#---------------------------------------------------------------------------

class GeneGP():
    """
    Classe de base représentant un gène dans le cadre de la programmation génétique.
    Chaque gène peut être un terminal (constante ou variable) ou une fonction (unaire ou binaire).

    Attributs de classe :
        - TYPE_GEN_NONE : type non spécifié.
        - TYPE_GEN_TERMINAL : terminal général.
        - TYPE_GEN_TERMINAL_SYMBOLE : terminal sous forme de symbole (variable).
        - TYPE_GEN_TERMINAL_INTEGER : terminal sous forme de constante entière.
        - TYPE_GEN_FONCTION : fonction générale.
        - TYPE_GEN_FONCTION_UNAIRE : fonction unaire.
        - TYPE_GEN_FONCTION_BINAIRE : fonction binaire.
    
    Attributs d'instance :
        - name_gen : nom du gène.
        - type_gen : type du gène (terminal ou fonction).
    """

    TYPE_GEN_NONE             =0
    TYPE_GEN_TERMINAL         =1
    TYPE_GEN_TERMINAL_SYMBOLE =2
    TYPE_GEN_TERMINAL_INTEGER =3
    TYPE_GEN_FONCTION         =4
    TYPE_GEN_FONCTION_UNAIRE  =5
    TYPE_GEN_FONCTION_BINAIRE =6

    len_terminal_set          =0
    max_N_valeur              =0
    dict_terminal_set         =None
    dict_functions            =None
    dict_listes_genes         =None
    dict_functions_type       =None
    def __init__(self,name_gen,type_gen=TYPE_GEN_NONE):
        """
        Initialise un gène avec un nom et un type donnés.
        Args :
            - name_gen (str) : nom du gène.
            - type_gen (int) : type du gène, par défaut TYPE_GEN_NONE.
        """

        self.name_gen=name_gen
        self.type_gen=type_gen

    def init_fonctions(config):
        """
        Initialise la liste dict_listes_genes.
        Args:
            config (obj):objet de config.
        """
  
        GeneGP.dict_functions=config.functions
        GeneGP.max_N_valeur=config.max_N_valeur
        
        function_All=config.funct_unaire.copy()+ config.funct_binaire.copy()
        function_All.sort()
        function_unaire =config.funct_unaire.copy()
        function_unaire.sort()
        function_binaire=config.funct_binaire.copy()
        function_binaire.sort()
        
        GeneGP.dict_terminal_set={}
        GeneGP.len_terminal_set= len(config.terminal_set)
        for i in range(GeneGP.len_terminal_set):
            GeneGP.dict_terminal_set[config.terminal_set[i]] =i
        GeneGP.dict_functions_type={}
        for x in config.funct_unaire:
             GeneGP.dict_functions_type[x]=True
        for x in config.funct_binaire:
             GeneGP.dict_functions_type[x]=False

        GeneGP.dict_listes_genes={
                                GeneGP.TYPE_GEN_NONE:[],
                                GeneGP.TYPE_GEN_TERMINAL_SYMBOLE:config.terminal_set,
                                GeneGP.TYPE_GEN_TERMINAL_INTEGER:[i for i in range(-1*config.max_N_valeur,config.max_N_valeur+1)],
                                GeneGP.TYPE_GEN_FONCTION:function_All ,
                                GeneGP.TYPE_GEN_FONCTION_UNAIRE:function_unaire,
                                GeneGP.TYPE_GEN_FONCTION_BINAIRE:function_binaire,
                                }
 

    def create_gene(type_gen,val=None):
        item=random.choice(GeneGP.dict_listes_genes[type_gen])
        if(val is not None): item=val
        if type_gen==GeneGP.TYPE_GEN_TERMINAL_SYMBOLE :
            pos=GeneGP.dict_terminal_set[item]
            return GenTerminalSymboleGP.create(item,GeneGP.len_terminal_set,pos)
        elif type_gen==GeneGP.TYPE_GEN_TERMINAL_INTEGER :
            return GenTerminalIntegerGP(item)
        elif type_gen==GeneGP.TYPE_GEN_FONCTION :
            if GeneGP.dict_functions_type[item]:
                return GenFonctionUnaireGP(item,GeneGP.dict_functions[item])
            else:
                return GenFonctionBinaireGP(item,GeneGP.dict_functions[item])
        elif type_gen==GeneGP.TYPE_GEN_FONCTION_UNAIRE :
            return GenFonctionUnaireGP(item,GeneGP.dict_functions[item])
        elif type_gen==GeneGP.TYPE_GEN_FONCTION_BINAIRE :
            return GenFonctionBinaireGP(item,GeneGP.dict_functions[item])
        else:
            return None

#------------------------------------------------------------------------
    def random_choice_fonction(): 
        """
        Choisit aléatoirement une fonction (unaire ou binaire).
        Returns:
            str: Une fonction aléatoire.
        """
        return GeneGP.create_gene(GeneGP.TYPE_GEN_FONCTION)

    def random_choice_fonction_unaire():
        """
        Choisit aléatoirement une fonction unaire.
        Returns:
            str: Une fonction unaire aléatoire.
        """
        return GeneGP.create_gene(GeneGP.TYPE_GEN_FONCTION_UNAIRE)

    def random_choice_fonction_binaire():
        """
        Choisit aléatoirement une fonction binaire.
        Returns:
            str: Une fonction binaire aléatoire.
        """
        return GeneGP.create_gene(GeneGP.TYPE_GEN_FONCTION_BINAIRE)

    def random_choice_terminal():
        """
        Choisit aléatoirement un terminal (avec possibilité de choisir une constante aléatoire).
        Returns:
            str/int: Un terminal aléatoire ou une constante.
        """
        if GeneGP.max_N_valeur>0 :
            if random.random() > 0.5:
                return GeneGP.create_gene(GeneGP.TYPE_GEN_TERMINAL_SYMBOLE)
            else:
                return GeneGP.create_gene(GeneGP.TYPE_GEN_TERMINAL_INTEGER) # 1 chance sur 2 d'avoir cte : sinon, on renvoie x 
        else:
            return GeneGP.create_gene(GeneGP.TYPE_GEN_TERMINAL_SYMBOLE)
#------------------------------------------------------------------------

    def read_str(type_gen,item):
        """
        Lit un gène à partir de sa représentation sous forme de texte.
        Args :
            - type_gen (int) : type du gène.
            - item (str) : représentation textuelle du gène.
        Returns :
            - Instance correspondante d'une sous-classe de GeneGP selon le type.
        """
        if type_gen==GeneGP.TYPE_GEN_TERMINAL_SYMBOLE :
            return GenTerminalSymboleGP.create(item)
        if type_gen==GeneGP.TYPE_GEN_TERMINAL_INTEGER :
            return GenTerminalIntegerGP(int(item))
        elif type_gen==GeneGP.TYPE_GEN_FONCTION_UNAIRE :
            fonction=GeneGP.dict_functions[item]
            return GenFonctionUnaireGP(item,fonction)
        elif type_gen==GeneGP.TYPE_GEN_FONCTION_BINAIRE :
            fonction=GeneGP.dict_functions[item]
            return GenFonctionBinaireGP(item,fonction)
        else:
            return None

    def write_str(self):
        """
        Représente le gène sous forme de texte.
        Returns :
            - (str) : représentation du gène sous la forme "nom:type".
        """
        return str(self.name_gen)+':'+str(self.type_gen)
#------------------------------------------------------------------------


    def is_terminal(self):
        """
        Indique si le gène est un terminal.
        Returns :
            - (bool) : False, car cette méthode est surchargée dans les sous-classes.
        """
        return False
    def is_fonction(self):
        """
        Indique si le gène est une fonction.
        Returns :
            - (bool) : False, car cette méthode est surchargée dans les sous-classes.
        """
        return False
    def is_fonction_unaire(self):
        """
        Indique si le gène est une fonction unaire.
        Returns :
            - (bool) : False, car cette méthode est surchargée dans les sous-classes.
        """
        return False
    def is_fonction_binaire(self):
        """
        Indique si le gène est une fonction binaire.
        Returns :
            - (bool) : False, car cette méthode est surchargée dans les sous-classes.
        """
        return False
    def evaluate(self,param1,param2):
        """
        Évalue le gène avec les paramètres donnés.
        Args :
            - param1 (float) : premier paramètre.
            - param2 (float) : second paramètre.
        Returns :
            - (float) : toujours 0 dans la classe de base.
        """
        return 0

#---------------------------------------------------------------------------
class GenTerminalGP(GeneGP):
    """
    Classe représentant un terminal (constante ou variable) dans la programmation génétique.
    """

    def __init__(self,name_gen,type_gen):
        super().__init__(name_gen,type_gen)
    def is_terminal(self):
        return True

class GenTerminalIntegerGP(GenTerminalGP):
    """
    Classe représentant un terminal sous forme de constante entière.
    """
    def __init__(self,name_gen):
        super().__init__(int(name_gen),self.TYPE_GEN_TERMINAL_INTEGER)

    def writeStr(self,param1="",param2=""):
        if(self.name_gen>0):
            return str(self.name_gen)
        else:
            return '('+str(self.name_gen)+')'

    def evaluate(self,param1,param2=0):
        return int(self.name_gen)

class GenTerminalSymboleGP(GenTerminalGP):
    """
    Classe représentant un gène terminal de type symbole.

    Un gène terminal de type symbole correspond à une variable utilisée dans une expression 
    (comme une variable x ou y dans une expression mathématique).

    Attributs :
    -----------
    posItem : int
        Position de la variable dans un tableau de valeurs (utile lorsqu'on évalue des expressions sur plusieurs variables).
    """
    def __init__(self,name_gen,posItem):
        super().__init__(name_gen,self.TYPE_GEN_TERMINAL_SYMBOLE)
        self.posItem=posItem

    def create(name,len_terminal_set=1,pos=0):
        if(len_terminal_set==1):
            return GenTerminalSymbole_simple_GP(name,pos)
        else:
            return GenTerminalSymbole_multiple_GP(name,pos)

    def writeStr(self,param1="",param2=""):
        return str(self.name_gen)

class GenTerminalSymbole_simple_GP(GenTerminalSymboleGP):
    """
    Classe représentant un gène terminal symbole simple, correspondant à une variable unique.
    """

    def evaluate(self,valeur,param2=0):
        return valeur
class GenTerminalSymbole_multiple_GP(GenTerminalSymboleGP):
    """
    Classe représentant un gène terminal symbole multiple, correspondant à une variable
    pouvant prendre différentes valeurs selon la position spécifiée.
    """

    def evaluate(self,valeur,param2=0):
        return valeur[self.posItem]
#---------------------------------------------------------------------------
class GenFonctionGP(GeneGP):
    """
    Classe de base pour les gènes de type fonction.
    
    Ce type de gène correspond à une fonction mathématique (par exemple addition, multiplication, sinus, etc.).
    """
    def __init__(self,name_gen,func,type_gen):
        super().__init__(name_gen,type_gen)
        self.func=func
    def is_terminal(self):
        return False
    def is_fonction(self):
        return True

class GenFonctionUnaireGP(GenFonctionGP):
    """
    Classe représentant une fonction unaire, c'est-à-dire une fonction prenant un seul paramètre 
    en entrée (comme sinus ou cosinus).
    """

    def __init__(self,name_gen,func):
        super().__init__(name_gen,func,self.TYPE_GEN_FONCTION_UNAIRE)

    def is_fonction_unaire(self):
        return True

    def writeStr(self,param1="",param2=""):
        return self.name_gen+"("+param1+")"

    def evaluate(self,param1=0,param2=0):
        return self.func(param1)


class GenFonctionBinaireGP(GenFonctionGP):
    """
    Classe représentant une fonction binaire, c'est-à-dire une fonction prenant deux paramètres 
    en entrée (comme addition, multiplication, etc.).
    """

    def __init__(self,name_gen,func):
        super().__init__(name_gen,func,self.TYPE_GEN_FONCTION_BINAIRE)

    def is_fonction_binaire(self):
        return True

    def writeStr(self,param1,param2):
        return "("+param1 + self.name_gen + param2+")"

    def evaluate(self,param1=0,param2=0):
        return self.func(param1,param2)
  


