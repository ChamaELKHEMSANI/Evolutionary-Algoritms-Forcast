# AlgoGP Web

Application web pour exécuter un algorithme de programmation génétique (GP) sur des données de type série temporelle ou données d'entrée/sortie, avec une interface graphique en navigateur et un mode CLI pour tests locaux.

## Vue d'ensemble

Ce projet permet de :

- charger des données depuis un fichier CSV ;
- configurer les paramètres de l'algorithme génétique ;
- lancer une recherche de formules mathématiques à partir des données ;
- visualiser les résultats, la convergence et les prédictions via une interface web ;
- valider le comportement de l'algorithme en ligne de commande.

Le backend est basé sur FastAPI et le frontend est livré dans le dossier 'frontend' avec du HTML/JavaScript et D3.js.

## Structure du projet

'''text
Web/
├── algo/                  # Implémentation du moteur GP
├── frontend/              # Interface utilisateur HTML/JS
├── tools/                 # Outils de configuration et mathématiques
├── main.py                # Serveur FastAPI web
├── maincli.py             # Version CLI pour exécution locale
├── requirements.txt       # Dépendances Python
├── web_callback_ext.py    # Callback WebSocket pour les messages temps réel
└── README.md              # Ce fichier
'''

## Prérequis

- Python 3.10+
- pip
- (recommandé) environnement virtuel

## Installation

Depuis le dossier 'Web' :

'''bash
cd Web
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
'''

## Lancement du serveur web

'''bash
cd Web
uvicorn main:app --reload
'''

Puis ouvrez dans le navigateur :

'''text
http://127.0.0.1:8000
'''

Le backend expose un WebSocket sur :

'''text
ws://127.0.0.1:8000/ws
'''

## Lancement en ligne de commande

Le projet inclut aussi un mode CLI pour tester le moteur GP sans navigateur :

'''bash
cd Web
python maincli.py --x 0,1,2,3 --y 0,1,4,9
'''

Ou en lisant un fichier de données :

'''bash
cd Web
python maincli.py --data-file ../data/sample.csv
'''

## Format des données

Les données attendues sont de type 'x,y' ou 'x ; y' en colonnes.

Exemple :

'''csv
0;0
1;1
2;4
3;9
4;16
'''

Le système utilise les points '(x, y)' pour estimer une formule pouvant approximer la relation.

## Paramètres principaux

La configuration est gérée côté serveur via 'ConfigToolsGP' et peut être ajustée depuis l'interface web. Les paramètres identifiés dans le projet incluent :

- 'size_population'
- 'size_echantillon'
- 'max_depth'
- 'max_iterations'
- 'max_N_valeur'
- 'seuil_fitness'
- 'tolerance_mutation'
- 'mode_selection'
- 'mode_mariage'
- 'mode_croisement'
- 'mode_remplacement'
- 'mode_mutation'
- 'funct_binaire'
- 'funct_unaire'

## Fonctionnement

1. L'utilisateur charge des données ou fournit des valeurs 'x' et 'y'.
2. Le backend construit une configuration pour le moteur GP.
3. Le moteur génère et évolue une population de formules.
4. Les meilleurs individus sont évalués par fitness.
5. Les résultats sont transmis en temps réel au navigateur via WebSocket.
6. La meilleure formule est affichée dans l'interface et utilisée pour prédire de nouvelles valeurs.

## Dépendances

Le fichier 'requirements.txt' contient les dépendances principales :

'''text
fastapi
uvicorn[standard]
websockets
numpy
'''

## Points d'attention

- Le projet s'appuie sur un algorithme de programmation génétique qui peut être coûteux en CPU selon la taille des données et les paramètres.
- Les performances dépendent fortement du nombre de générations, de la population et de la profondeur maximale.
- Les fonctions mathématiques et la normalisation peuvent changer selon les données à modéliser.

## Projets associés

Le dossier parent contient également des variantes plus générales ou desktop du même moteur. Ce dossier 'Web' est la version accessible depuis navigateur.

## Licence

Ce projet est fourni tel quel pour usage local ou de développement. Vérifiez la licence globale du dépôt si vous souhaitez réutiliser le code dans un contexte commercial ou public.

## Auteur / contribution

Chama EL KHEMSANI
