#!/usr/bin/env python3
"""CLI pour tester l'algorithme sans WebSocket
Usage: python maincli.py --x 0,1,2 --y 0,1,4 [options]
Or: python maincli.py --data-file ../../data/sample.csv
"""
import argparse
import sys
import json
import os
from datetime import datetime
from pathlib import Path

from algo.algoGP import AlgoGP
from tools.configToolsGP import ConfigToolsGP


class SimpleCallback:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.best_result = None

    def set_jauge_value(self, str_message, pos_value, max_value):
        if self.verbose:
            print(f"[Progress] {pos_value}/{max_value} - {str_message}")

    def affiche_chromosome(self, iteration, chromosome, inputs=None, elapsed=None, min_val=None, max_val=None ):
        self.best_result = chromosome
        if self.verbose:
            formule=chromosome.formule
            if min_val is not None and max_val is not None:
                # Normalisation de la formule   
                ecart_val= max_val- min_val
                if ecart_val==0:
                    ecart_val=1
                formule=str(ecart_val)+'*('+ formule +') +'+ str(min_val)   
            s = f"iter={iteration} fitness={chromosome.fitness} normalise: {min_val}/{max_val}  depth={chromosome.depth} formula={formule}"
            if elapsed is not None:
                s += f" elapsed={elapsed:.2f}s"
            print(s)

    def affiche_resultats(self, min_val=None, max_val=None ):
        if self.best_result is not None:
            print("=== RESULT ===")
            print(f"best_fitness: {self.best_result.fitness}")
            print(f"normalise: {min_val} {max_val}")
            formule=self.best_result.simplifyFormule()
            if min_val is not None and max_val is not None:
                # Normalisation de la formule   
                ecart_val= max_val- min_val
                if ecart_val==0:
                    ecart_val=1
                formule=str(ecart_val)+'*('+ formule +') +'+ str(min_val)  
            print(f"best_formula: {formule}")


def parse_list(s):
    if s is None or s == "":
        return []
    parts = [p.strip() for p in s.split(',') if p.strip() != '']
    out = []
    for p in parts:
        try:
            if '.' in p:
                out.append(float(p))
            else:
                out.append(int(p))
        except Exception:
            out.append(p)
    return out


def read_xy_from_file(path):
    x = []
    y = []
    path = Path(path)
    if not path.exists():
        return x, y
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # try semicolon, comma, or whitespace
            if ';' in line:
                parts = line.split(';')
            elif ',' in line:
                parts = line.split(',')
            else:
                parts = line.split()
            if len(parts) < 2:
                continue
            a = parts[0].strip()
            b = parts[1].strip()
            try:
                aval = float(a) if '.' in a else int(a)
            except Exception:
                try:
                    aval = float(a)
                except Exception:
                    aval = a
            try:
                bval = float(b) if '.' in b else int(b)
            except Exception:
                try:
                    bval = float(b)
                except Exception:
                    bval = b
            x.append(aval)
            y.append(bval)
    return x, y


def main():
    parser = argparse.ArgumentParser(description='Run AlgoGP locally without WebSocket')
    parser.add_argument('--x', required=False, help='Comma separated x values e.g. 0,1,2')
    parser.add_argument('--y', required=False, help='Comma separated y values e.g. 0,1,4')
    parser.add_argument('--data-file', default='../../data/sample.txt',required=False, help='Data file to read x,y from')
    parser.add_argument('--output-file', default='../../output/out.txt', required=False, help='Output file path. If omitted, defaults to output/test_YYYY_MM_DD_HH_MM_SS.txt')
    parser.add_argument('--size_population', type=int,default=200,required=False)
    parser.add_argument('--size_echantillon', type=int,default=100,required=False)
    parser.add_argument('--max_depth', type=int,default=5,required=False)
    parser.add_argument('--max_iterations', type=int,default=1000,required=False)
    parser.add_argument('--max_N_valeur', type=int,default=10,required=False)
    parser.add_argument('--seuil_fitness', type=float,default=0.01,required=False)
    parser.add_argument('--tolerance_mutation', type=float,default=0.5 ,required=False)
    parser.add_argument('--mode_selection',type=str,default='best', required=False)
    parser.add_argument('--mode_mariage',type=str,default='extrem',required=False)
    parser.add_argument('--mode_croisement',type=str,default='swap-middle',required=False)
    parser.add_argument('--mode_remplacement',type=str,default='mixt_best',required=False)
    parser.add_argument('--mode_mutation',type=str, default='replace',required=False)
    parser.add_argument('--verbose',type=bool, default=True,required=False)
    args = parser.parse_args()

    inputs = []
    outputs = []

    # Priority: explicit --x/--y > data-file > default data file in repo
    if args.x and args.y:
        inputs = parse_list(args.x)
        outputs = parse_list(args.y)
    else:
        # determine candidate data file
        candidates = []
        if args.data_file:
            candidates.append(args.data_file)
        # default relative to this script: go to repo root data/sample.txt or sample.csv
        script_dir = Path(__file__).resolve().parent
        repo_root = script_dir.parent.parent
        candidates.append(str(repo_root / 'data' / 'sample.txt'))
        candidates.append(str(repo_root / 'data' / 'sample.csv'))
        # try candidates
        for c in candidates:
            xi, yi = read_xy_from_file(c)
            if xi and yi:
                inputs = xi
                outputs = yi
                if args.verbose:
                    print(f"Loaded {len(inputs)} pairs from {c}")
                break

    if len(inputs) == 0 or len(outputs) == 0:
        print('Error: no data available. Provide --x and --y or a valid --data-file')
        sys.exit(1)
    if len(inputs) != len(outputs):
        print('Error: x and y must have same length')
        sys.exit(1)

    config = ConfigToolsGP(None)
    if args.size_population is not None:
        config.size_population = args.size_population
    if args.size_echantillon is not None:
        config.size_echantillon = args.size_echantillon
    if args.max_depth is not None:
        config.max_depth = args.max_depth
    if args.max_iterations is not None:
        config.max_iterations = args.max_iterations
    if args.max_N_valeur is not None:
        config.max_N_valeur = args.max_N_valeur
    if args.seuil_fitness is not None:
        config.seuil_fitness = args.seuil_fitness
    if args.tolerance_mutation is not None:
        config.tolerance_gene_Mutate = 1 - args.tolerance_mutation
    if args.mode_selection is not None:
        config.mode_selection = args.mode_selection
    if args.mode_mariage is not None:
        config.mode_mariage = args.mode_mariage
    if args.mode_croisement is not None:
        config.mode_croisement = args.mode_croisement
    if args.mode_remplacement is not None:
        config.mode_remplacement = args.mode_remplacement
    if args.mode_mutation is not None:
        config.mode_mutation = args.mode_mutation

    callback = SimpleCallback(verbose=args.verbose)
    algo = AlgoGP()
    algo.initialise(config, inputs, outputs, callback)

    try:
        algo.execute()
    except KeyboardInterrupt:
        algo.setStop()
        print('Interrupted')

    best = algo.get_best()
    if best is not None:
        best.denormalise(min_val=algo.min_val, max_val=algo.max_val)
        print('\nFinal best:')
        print('fitness =', best.fitness)
        print('formula =', best.formule)
        try:
            if algo.min_val is not None and algo.max_val is not None:
                # Normalisation de la formule   
                ecart_val= algo.max_val- algo.min_val
                if ecart_val==0:
                    ecart_val=1
                y_pred = [ecart_val*best.evaluate(xi)+algo.min_val for xi in inputs]    
            print('y_pred =', y_pred)
        except Exception:
            y_pred = None

        if args.output_file:
            output_path = Path(args.output_file)
        else:
            out_dir = Path(__file__).resolve().parent / '..' / 'output'
            out_dir = out_dir.resolve()
            out_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            output_path = out_dir / f'test_{timestamp}.txt'

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open('w', encoding='utf-8') as f:
            f.write('fitness=' + str(best.fitness) + '\n')
            f.write('formula=' + str(best.formule) + '\n')
            f.write('formulaSimplify=' + str(best.simplifyFormule()) + '\n')
            if y_pred is not None:
                f.write('y_pred=' + json.dumps(y_pred) + '\n')
            f.write('x=' + json.dumps(inputs) + '\n')
            f.write('y=' + json.dumps(outputs) + '\n')

        print(f'Written results to {output_path}')
    else:
        print('No result')


if __name__ == '__main__':
    main()
