# backend/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import json
import asyncio
import sys
import os

# Ajouter le chemin parent pour importer le package algo
sys.path.append(os.path.dirname(__file__))

from algo.algoGP import AlgoGP
from tools.configToolsGP import ConfigToolsGP
from web_callback_ext import WebCallback


app = FastAPI()

@app.get("/")
async def get_index():
    return FileResponse("./frontend/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        params = json.loads(data)
        inputs = params.get('x', [])
        outputs = params.get('y', [])
        if not inputs:
            await websocket.send_text(json.dumps({'type': 'error', 'message': 'Aucune donnée'}))
            return

        # --- Configuration ---
        config = ConfigToolsGP(None)   # ou instanciation avec paramètres
        config.size_population = params.get('size_population', 200)
        config.size_echantillon = params.get('size_echantillon', 50)
        config.max_depth = params.get('max_depth', 5)
        config.max_iterations = params.get('max_iterations', 50)
        config.max_N_valeur = params.get('max_N_valeur', 10)
        config.seuil_fitness = params.get('seuil_fitness', 0.01)
        # adaptez selon vos attributs : config.tolerance_gene_Mutate, etc.
        # Par exemple :
        config.tolerance_gene_Mutate = 1 - params.get('tolerance_mutation', 0.7)
        config.terminal_set = ['x']
        funct_binaire = params.get('funct_binaire')
        if isinstance(funct_binaire, list) and len(funct_binaire) > 0:
            config.funct_binaire = funct_binaire
        else:
            config.funct_binaire = ['+', '-', '*', '**', '/']   # selon votre config

        funct_unaire = params.get('funct_unaire')
        if isinstance(funct_unaire, list) and len(funct_unaire) > 0:
            config.funct_unaire = funct_unaire
        else:
            config.funct_unaire = ['sin','cos','ln','sqrt','tan','ctg','e','tanh','abs']

        config.mode_selection = params.get('mode_selection', 'best')
        config.mode_mariage = params.get('mode_mariage', 'extrem')
        config.mode_croisement = params.get('mode_croisement', 'swap-middle')
        config.mode_remplacement = params.get('mode_remplacement', 'mixt_best')
        config.mode_mutation = params.get('mode_mutation', 'replace')
        config.startValue = int(params.get('startValue',0))
        config.horizon = int(params.get('horizon', 0))
        #print("Config:", config.__dict__)
        # --- Callback Web ---
        loop = asyncio.get_event_loop()
        callback = WebCallback(websocket, loop)

        # --- Initialisation de l'algorithme ---
        # Votre AlgoGP attend probablement un widget dans initialise.
        # On va passer le callback à la place.
        # Vous devrez modifier légèrement algoGP.py pour accepter un objet "widget" qui
        # possède set_jauge_value, affiche_chromosome, affiche_resultats.
        # Heureusement, WebCallback a ces méthodes.

        # Création de l'algo
        algo = AlgoGP()
        # Appel de initialise avec le callback (au lieu du widget)
        algo.initialise(config, inputs, outputs, callback)

        # Lancer l'algorithme (en thread séparé pour ne pas bloquer)
        await loop.run_in_executor(None, algo.execute)

        # Une fois terminé, on peut envoyer un message final
        await websocket.send_text(json.dumps({'type': 'done'}))

    except WebSocketDisconnect:
        print("Client déconnecté")
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        await websocket.send_text(json.dumps({'type': 'error', 'message': str(e)}))
