import argparse



class  ArgParseToolsGP():
    """
    Classe pour la gestion des arguments passés en ligne de commande.
    Cette classe permet de configurer l'algorithme de programmation génétique via divers paramètres.
    """
    def __init__(self):
        self.args={}  # Dictionnaire pour stocker les arguments analysés.

    def parse_arguments(self):
        """
        Méthode pour analyser les arguments passés en ligne de commande et les stocker dans un dictionnaire.
        """
        parser = argparse.ArgumentParser(description='Apprentissage de fonction par Genetic Programming',epilog="les paramètres doivent être en minuscule")
        parser.add_argument('-mode','--mode', help='Mode de traitement', required=False, choices=('run', 'dialogue', '2d','multi','populate','iterate','draw','test'),default="dialogue")

        # Ajout des différents arguments acceptés.
        parser.add_argument('-nc','--nombre_coordonees', help='Nombre de coordonnées (Inutile en dehors du mode MULTI)',required=False,default=3,type=int)#######################################################
        parser.add_argument('-sp','--size_population', help='Taille de la population', required=False,default=200,type=int)
        parser.add_argument('-n','--max_N_valeur', help='Valeur maximale pour les constantes', required=False,default=10,type=int)
        parser.add_argument('-e','--size_echantillon', help="Dimension de l'échantillon", required=False,default=75,type=int)
        parser.add_argument('-d','--size_depth', help="Profondeur de l'arbre", required=False,default=5,type=int)
        parser.add_argument('-nbrun','--nb_iterations', help="Nombre d'itérations", required=False,default=20,type=int)
        parser.add_argument('-xmin','--xmin', help='Valeur minimum de x', required=False,default=0,type=int)
        parser.add_argument('-xmax','--xmax', help='Valeur maximum de x', required=False,default=10,type=int)
        parser.add_argument('-ymin','--ymin', help='Valeur minimum de y', required=False,default=0,type=int)
        parser.add_argument('-ymax','--ymax', help='Valeur maximum de y', required=False,default=1,type=int)
        parser.add_argument('-tl','--tolerance_gene_Length', help='Tolerance Longueur génétique', required=False,default=1,type=float)
        parser.add_argument('-tm','--tolerance_gene_Mutate', help='Tolerance Mutation génétique', required=False,default=0.3,type=float)
        parser.add_argument('-sf','--seuil_fitness', help='Seuil fitness arret', required=False,default=0.01,type=float)
        parser.add_argument('-f','--formule', help='Equation de la formule', required=False,default="")
        parser.add_argument('-s','--seed', help='Graine de la géneration aléatiore ', required=False,default=123456789,type=int)
        parser.add_argument('-v','--verbose', help='verbose', required=False, action="store_true")
        parser.add_argument('-duree','--duree_maximum', help="Duree maximum d'execution", required=False,default=60*60*24,type=int)

        parser.add_argument('-t','--bl_thread', help='lance via un thread', required=False, action="store_true")
        parser.add_argument('-out','--outputfile', help='Fichier de sortie', required=False,default="")
        parser.add_argument('-in','--inputfile', help="Fichier d'entrée", required=False,default="")
        parser.add_argument('-pf','--population_file', help="Fichier de populations", required=False,default="")

        parser.add_argument('-iter_field','--iter_field', help='iter_field', required=False,default="")
        parser.add_argument('-iter_min','--iter_min', help='iter_min', required=False,default=0,type=int)
        parser.add_argument('-iter_max','--iter_max', help='iter_max', required=False,default=1,type=int)
        parser.add_argument('-iter_step','--iter_step', help='iter_step', required=False,default=1,type=int)

        parser.add_argument('-draw_file','--draw_file', help='draw_file', required=False,default="")
        parser.add_argument('-draw_field_x','--draw_field_x', help='draw_field_x', required=False,default="")
        parser.add_argument('-draw_field_y','--draw_field_y', help='draw_field_y', required=False,default="")

        parser.add_argument('-selection','--selection', help="Mode de sélection", required=False, choices=("best", "worst", "rand"),default="best")
        parser.add_argument('-mariage','--mariage', help='Mode de mariage', required=False, choices=("best", "extrem", "rand"),default="extrem")
        parser.add_argument('-croisement','--croisement', help='Mode de croisement', required=False, choices=("swap-middle", "absorp-partielle", "absorp-totale"),default="swap-middle")
        parser.add_argument('-mutation','--mutation', help='Mode de mutation', required=False, choices=("replace", "swap", "deplace"),default="replace")
        parser.add_argument('-remplacement','--remplacement', help='Mode de remplacement', required=False, choices=("mixt_best", "child_only", "child_add","mixt_rand"),default="mixt_best")
 


        # Stockage des arguments dans un dictionnaire.
        self.args = vars(parser.parse_args())
        self.read_arguments()

    def read_arguments(self):
        """
        Méthode pour lire les arguments stockés et les assigner à des attributs de la classe.
        """

        for key, val in self.args.items():
            setattr(self, key, val)

    def deepcopy(self):
        """
        Crée une copie profonde de l'objet courant.
        Returns:
            ArgParseToolsGP: Une nouvelle instance avec les mêmes arguments.
        """
        item=ArgParseToolsGP()
        item.args=self.args.copy()
        item.read_arguments()
        return item

		