import sys
import math
from collections import defaultdict
from scipy.spatial import distance
import numpy as np
import itertools

capture_patterns = {0: [[1, 3]],
 1: [[0, 2], [0, 4], [2, 4], [0, 2, 4]],
 2: [[1, 5]],
 3: [[0, 4], [0, 6], [4, 6], [0, 4, 6]],
 4: [[1, 3],
  [1, 5],
  [1, 7],
  [3, 5],
  [3, 7],
  [5, 7],
  [1, 3, 5],
  [1, 3, 7],
  [1, 5, 7],
  [3, 5, 7],
  [1, 3, 5, 7]],
 5: [[8, 2], [8, 4], [2, 4], [8, 2, 4]],
 6: [[3, 7]],
 7: [[8, 4], [8, 6], [4, 6], [8, 4, 6]],
 8: [[5, 7]]}


def debug(txt):
    print(txt,file=sys.stderr,flush=True)

class Case:
    def __init__(self,number,value):
        self.number = 0
        self.color = ""
        self.value = value
        self.neighbors = []

class Plateau:
    def __init__(self,init_values):
        self.cases = {k:iv for k,iv in enumerate(init_values)}
        self.capture_patterns = capture_patterns

    def play(self):
        # Get index of empty cases

        # Get associated capture patterns



# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# depth = int(input())
initial_values = []

# for i in range(3):
#     for j in input().split():
#         initial_values.append(int(j))
        
initial_values = [1,0,0,3,2,1,0,1,5]

p = Plateau(initial_values) 





p.play()


# print(depth,file=sys.stderr,flush=True)

# # Write an action using print
# # To debug: print("Debug messages...", file=sys.stderr, flush=True)

# print("0")
