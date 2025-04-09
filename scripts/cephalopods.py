
import sys
import math
from collections import defaultdict
from scipy.spatial import distance
import numpy as np
import itertools
import uuid 


class Grid:
    def __init__(self, values,factor=1,parent_id=None):
        self.values = values
        self.factor = factor
        self.parent_id = parent_id
        self.id = self.__int__()
        
    def update_id(self):
        self.id = self.__int__()

    def get_zeros_index(self):
        return [k for k,v in self.values.items() if v == 0]    
        
    def __int__(self):
        return int("".join(map(str,(i for i in self.values.values()))))

    def __str__(self):
        return str(self.values)

    def __hash__(self):
        return hash(str(self))

    def get(self,i):
        return self.values.get(i)

    def __eq__(self,other):
        return self.values == other.values
    
    def copy(self,v,f,i):
        return Grid(v,f,i)

    def update(self,d):
        self.values.update(d)
        
    def items(self):
        return self.values.items()
    
    def set_factor(self,f):
        self.factor = f

def get_patterns_list(height,width):
    cases = []
    for nr in range(height):
        for nc in range(width):
            cases.append((nr,nc))
            
    dist = distance.cdist(cases, cases, 'euclidean')
            
    groups = defaultdict(list)
    for key, value in np.argwhere(dist==1):
        groups[key].extend([key, value])

    groups = list(map(set,list(groups.values())))

    patterns = {}
    for k,g in enumerate(groups):
        combinations = []
        for i in range(3,6):
            c = list(itertools.combinations(g,i))
            combinations.append(c)
        combinations = list(itertools.chain(*combinations))
        combinations = [list(map(int,i)) for i in combinations if k in i]
        combinations = [[i for i in x if i != k] for x in combinations]
        patterns[k] = combinations

    patterns_list = []
    for k in patterns.keys():
        for v in patterns[k]:
            patterns_list.append((k,v))
        
    return patterns_list

def debug(txt):
    print(txt,file=sys.stderr,flush=True)

def compute(patterns,grid=None):
    '''
    La fonction "compute" traite chaque grille unitairement pour évaluer les prochains coups 
    Tout d'abord, elle identifie les zéros présent dans la grille. Pour chaque index où la valeur
    est égale à zéro, on récupère l'ensemble des patterns de capture associés (les patterns sont des tableaux d'entiers),
    '''
    states = {k:{"capture":set(),"non_capture":set()} for k in range(9)}
    # result = set()
    zeros = list(grid.get_zeros_index())
    # print(zeros)
    if len(zeros) != 0:
        for zero,pattern_index in filter(lambda x : x[0] in zeros,patterns):
            # print(zero,pattern_index)
            g = grid.copy(grid.values.copy(),grid.factor,grid.id)
            s = sum(g.get(p) for p in pattern_index)
            if (s <= 6) and (0 not in (g.get(p) for p in pattern_index)):
                g.update({p:0 for p in pattern_index})
                g.update({zero:s})
                g.update_id() 
                states[zero]["capture"].add(g)
                states[zero]["non_capture"] = set()
            else:
                if (len(states[zero]["capture"]) == 0) and (len(states[zero]["non_capture"]) == 0):
                    g.update({zero:1})
                    g.update_id() 
                    states[zero]['non_capture'].add(g)
        r = list(states.get(z).get(c) for c in ["capture","non_capture"] for z in zeros if len(states.get(z).get(c)) != 0)
        r = list(item for subset in r for item in subset)
        # print(r)
        return r
    else:
        return {grid}

def resolve(val,patterns):
    '''
    La fonction "resolve" est une fonction récursive pour appliquer le traitement sur les données.
    
    :param val: Le paramètre val est une liste de dictionnaire représentant les différentes grilles après chaque coup 
    :param patterns: La liste patterns contient l'ensemble des patterns de captures sur une grille de dimension donnée
    :return: La fonction retourne une liste de grille (dict)  
    '''
    #On récupère au sein de la fonction la variable "depth" pour monitorer le nombre de tour qu'il reste
    global depth
    global hashes
    # print(f"Tour {depth}")
    # final_results = []
    #Execution de la fonction "compute" dans un map pour évaluer toutes les options de jeux sur chaque grille dans la liste "val"
    # final_results+=list(itertools.chain(*list(map(lambda x : compute(patterns,x),val))))
    # final_results = [(i.id,i.parent_id,i.factor,i) for i in list(itertools.chain(*list(map(lambda x : compute(patterns,x),val))))]

    fr = [i for i in list(itertools.chain(*list(map(lambda x : compute(patterns,x),val))))]
    dict_fr = {i.id:i for i in fr}
    ids_count = {i.id:fr.count(i) for i in fr if fr.count(i) > 1}
    end_state = []

    if len(ids_count) > 0:
        for i,n in ids_count.items():
            total_factor = sum(map(lambda x : x.factor,list(filter(lambda x : x.id == i,fr))))
            if '0' not in str(i):       
                    end_state += [i]
                    hashes += [i]*total_factor
            else:
                    dict_fr[i].set_factor(total_factor)
                    
    reload = [v for k,v in dict_fr.items() if k not in end_state]
    
    if all(map(lambda x : 0 not in x.values.values(),reload)):
        return []
    else:
        depth -= 1
        if depth == 0:
            return reload
        else:
            return resolve(reload,patterns)

update = lambda j,k: (j+k)%2**30
   
patterns = [(0, [1, 3]),
 (1, [0, 2]),
 (1, [0, 4]),
 (1, [2, 4]),
 (1, [0, 2, 4]),
 (2, [1, 5]),
 (3, [0, 4]),
 (3, [0, 6]),
 (3, [4, 6]),
 (3, [0, 4, 6]),
 (4, [1, 3]),
 (4, [1, 5]),
 (4, [1, 7]),
 (4, [3, 5]),
 (4, [3, 7]),
 (4, [5, 7]),
 (4, [1, 3, 5]),
 (4, [1, 3, 7]),
 (4, [1, 5, 7]),
 (4, [3, 5, 7]),
 (4, [1, 3, 5, 7]),
 (5, [8, 2]),
 (5, [8, 4]),
 (5, [2, 4]),
 (5, [8, 2, 4]),
 (6, [3, 7]),
 (7, [8, 4]),
 (7, [8, 6]),
 (7, [4, 6]),
 (7, [8, 4, 6]),
 (8, [5, 7])]
init = {0: 3, 1: 0, 2: 0, 3: 3, 4: 6, 5: 2, 6: 1, 7: 0, 8: 2}
depth = 24
hashes = []


def main():
    g = Grid(init)
    r = resolve([g],patterns)
    hashes = []
    for i in r:
        hashes += [int(i)]*i.factor
    r = list(itertools.accumulate(hashes,update))[-1]
    print(r)
    if r == 661168294:
        print("Test 6 : OK")

if __name__ == "__main__":
    main()