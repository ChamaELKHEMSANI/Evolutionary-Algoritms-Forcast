# backend/web_callback_ext.py
import json
import asyncio
from sympy import symbols, simplify

class WebCallback:
    """
    Callback WebSocket amélioré : calcule `y_pred` si on fournit les `inputs`.
    """
    def __init__(self, websocket, loop):
        self.websocket = websocket
        self.loop = loop
        self.best_result = None

    def set_jauge_value(self, str_message, pos_value, max_value):
        self._send({
            'type': 'progress',
            'message': str_message,
            'value': pos_value,
            'max': max_value
        })

    def affiche_chromosome(self, iteration, chromosome, inputs=None, elapsed=None, min_val=None, max_val=None):
        # stocker le meilleur
        try:
            self.append_result(chromosome)
        except Exception:
            pass
 
        y_pred = None
        if inputs:
            try:
                if min_val is not None and max_val is not None:
                    # Normalisation de la formule   
                    ecart_val= max_val- min_val
                    if ecart_val==0:
                        ecart_val=1
                    y_pred = [ecart_val*chromosome.evaluate(xi)+min_val for xi in inputs]    
                else:
                    y_pred = [chromosome.evaluate(xi) for xi in inputs]
            except Exception:
                y_pred = None

        formule=chromosome.formule
        if min_val is not None and max_val is not None:
            # Normalisation de la formule   
            ecart_val= max_val- min_val
            if ecart_val==0:
                ecart_val=1
            formule=str(ecart_val)+'*('+ formule +') +'+ str(min_val) 

        msg = {
            'type': 'update',
            'iteration': iteration,
            'fitness': chromosome.fitness,
            'formula': formule,
            'generation': chromosome.generation,
        }
        if y_pred is not None:
            msg['y_pred'] = y_pred

        if elapsed is not None:
            msg['elapsed'] = elapsed

        self._send(msg)


    def affiche_resultats(self, inputs, outputs, min_val=None, max_val=None,startValue=0,horizon=0) :
        if self.best_result is not None:
            best = self.best_result
            fitness=best.fitness
            y_pred = None
            if inputs:
                try:
                    if min_val is not None and max_val is not None:
                        # Normalisation de la formule   
                        ecart_val= max_val- min_val
                        if ecart_val==0:
                            ecart_val=1
                        y_pred = [ecart_val*best.evaluate(xi)+min_val for xi in inputs]    
                    else:
                        y_pred = [best.evaluate(xi) for xi in inputs]
                except Exception:
                    y_pred = None

            yForcast = None
            if startValue is not None and horizon is not None and horizon > 0:
                try:
                    if min_val is not None and max_val is not None:
                    # Normalisation de la formule   
                        ecart_val= max_val- min_val
                        if ecart_val==0:
                            ecart_val=1
                        yForcast = [ecart_val*best.evaluate(xi)+min_val for xi in range(startValue, startValue+horizon)]    
                    else:
                        yForcast = [best.evaluate(xi) for xi in range(startValue, startValue+horizon)]
                except Exception:
                    yForcast = None 
            self._send({
                'type': 'done',
                'best_fitness': fitness,
                'best_formula': self._simplify(best.formule,min_val, max_val),
                'y_pred': y_pred,
                'yForcast': yForcast,
            })


    def _simplify(self,formule,min_val=None, max_val=None):
        try:
            x = symbols('x')
            if min_val is not None and max_val is not None:
                # Normalisation de la formule   
                ecart_val= max_val- min_val
                if ecart_val==0:
                    ecart_val=1
                formule=str(ecart_val)+'*('+ formule +') +'+ str(min_val)
            simp_formule = str(simplify(formule))  
            print(f"Formule simplifiée:  {formule} : {simp_formule}") 
            return simp_formule
        except Exception as e:
            print(f"Erreur lors de la simplification de l'expression: {formule}")
            return formule


    def _send(self, data):
        asyncio.run_coroutine_threadsafe(
            self.websocket.send_text(json.dumps(data)),
            self.loop
        )

    def append_result(self, best):
        self.best_result=best
