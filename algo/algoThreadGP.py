import threading
from algo.algoGP import AlgoGP

"""
La classe AlgoThreadGP est une extension de la classe AlgoGP qui intègre la gestion multi-thread via la classe threading.Thread. 
Elle permet d'exécuter l'algorithme génétique dans un thread séparé, offrant une meilleure réactivité de l'interface utilisateur ou d'autres parties de l'application pendant les calculs intensifs.

Avantages de AlgoThreadGP
	Multi-threading : Permet une exécution en arrière-plan sans bloquer l'interface graphique ou d'autres tâches.
	Gestion de l'arrêt : L'utilisateur peut interrompre proprement l'exécution en temps réel.
	Héritage de AlgoGP : Réutilise toutes les fonctionnalités de la classe de base.

Attributs principaux
	Hérités de AlgoGP
		population : Liste des individus de la population.
		func_set : Ensemble des fonctions unaires et binaires.
		terminal_set : Ensemble des terminaux (variables ou constantes).
		max_iterations : Nombre maximal d'itérations.
		inputs et outputs : Données d'entrée et de sortie pour l'évaluation des individus.
		widget : Interface graphique associée pour l'affichage des résultats.
	Nouveaux attributs
		_stop_event : Instance de threading.Event utilisée pour indiquer si le thread doit s'arrêter.

Méthodes principales
1. Initialisation : __init__
	Hérite des initialisations de AlgoGP et de threading.Thread.
	Configure un événement _stop_event pour gérer l'arrêt du thread.
2. Démarrage du thread : run
	Marque l'algorithme comme en cours d'exécution (isRunning = True).
	Appelle la méthode execute de AlgoGP pour exécuter l'algorithme.
	Une fois terminé, met à jour le statut (isRunning = False).
3. Arrêt du thread : stop
	Met à jour l'attribut isRunning pour indiquer que l'algorithme doit s'arrêter.
	Déclenche l'événement _stop_event, signalant au thread qu'il doit terminer son exécution.
4. Vérification de l'arrêt : isStop
	Vérifie l'état de _stop_event.
	Utilisé pour interrompre les boucles ou les calculs lorsque l'utilisateur demande l'arrêt.

Héritage de méthodes
	Les méthodes suivantes sont héritées de AlgoGP et restent disponibles dans AlgoThreadGP :

	Initialisation et gestion de la population : initialise, populate.
	Évaluation des individus : evaluate_Terminal, evaluate_fonction_Unaire, evaluate_fonction_Binaire.
	Sélection, croisement et mutation : selection, __replace_worst.
	Exécution principale : execute.

Diagramme de séquence
	L'utilisateur initialise une instance de AlgoThreadGP.
	Les paramètres de l'algorithme sont configurés via initialise.
	Le thread est démarré avec start (appelant run en arrière-plan).
	L'algorithme génétique s'exécute en boucle (execute).
	Si l'utilisateur souhaite arrêter l'algorithme, stop est appelé, ce qui déclenche l'événement _stop_event.
	Le thread se termine proprement après avoir vérifié isStop.
"""

class AlgoThreadGP(AlgoGP,threading.Thread):
    def __init__(self):
        """
        Initialise une instance d'algorithme génétique multi-thread.
        Args:
        """
        threading.Thread.__init__(self)
        AlgoGP.__init__(self)
        self._stop_event = threading.Event()

    def stop(self):
        """
        Arrête l'exécution du thread en déclenchant l'événement d'arrêt.
        """
        self._stop_event.set()

    def isStop(self):
        """
        Vérifie si l'événement d'arrêt a été déclenché.

        Returns:
            bool: True si l'algorithme doit s'arrêter, False sinon.
        """
        return self._stop_event.is_set()

    def run(self):
        """
        Démarre l'exécution de l'algorithme génétique dans un thread séparé.
        """

        self.execute()      



