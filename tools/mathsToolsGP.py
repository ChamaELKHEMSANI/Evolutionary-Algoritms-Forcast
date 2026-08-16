import sys
import random
import math
import numpy as np
import importlib  
#from sympy import Symbol,sympify
"""
La classe MathsToolsGP est une boîte à outils mathématiques qui semble être utilisée dans le cadre de l'évaluation d'expressions génétiques. Elle contient différentes méthodes permettant de gérer des terminaux, des fonctions unaires et binaires, ainsi que de manipuler des gènes sous forme de liste
"""
class MathsToolsGP():
    """
    Classe contenant les outils mathématiques pour l'évaluation des expressions génétiques.
    Elle fournit des méthodes pour générer des terminaux, évaluer des fonctions unaires et binaires,
    et manipuler des gènes sous forme de chaînes de caractères.
    """
    sympy_valide=False
    sympy_module=None
 
 #------------------------------------------------------------------------
    def evaluate_formule(formule_texte,**kwargs):
        """
        Évalue une formule mathématique sous forme de chaîne de caractères.
        Args:
            formule_texte (str): La formule à évaluer.
            kwargs (dict): Les variables à insérer dans la formule.
        Returns:
            float: Le résultat de l'évaluation de la formule.
        """
        available_functions = {
                                'sin': np.sin,
                                'cos': np.cos,
                                'e': np.exp,
                                'ln':  np.log,
                                'tan': np.tan,
                                'ctg': lambda x:1/np.tan(x),
                                'sqrt': np.sqrt,
                                'tanh': np.tanh,
                                }


        try:
            return  eval(formule_texte, available_functions, kwargs)
        except Exception as ex:
            print(ex)
            return 0

#------------------------------------------------------------------------
    def simplifie_formule_dynamique(formule_texte):
        if MathsToolsGP.sympy_valide==None:
            try:
                print("simplifie_formule")
                MathsToolsGP.sympy_module = importlib.import_module("sympy")  
                #from sympy import Symbol,sympify,simplify
                MathsToolsGP.sympy_valide=True
                print("sympy_valide=True")
            except Exception as exp:
                print(exp)
                MathsToolsGP.sympy_valide=False

        if MathsToolsGP.sympy_valide==False:
            return formule_texte
        formule_memorise=formule_texte
        try:
            x  = MathsToolsGP.sympy_module.Symbol('x', real = True)
            return  str(MathsToolsGP.sympy_module.sympify(formule_texte, {"x": x}) )
        except Exception as exp:
            print(exp)
            return formule_memorise

    def simplifie_formule(formule_texte):
        """
        formule_memorise=formule_texte
        try:
            x  = Symbol('x', real = True)
            return  str(sympify(formule_texte, {"x": x}) )
        except Exception as exp:
            print(exp)
            return formule_memorise
        """
        return  formule_texte


