#!/usr/bin/env python
import pdb
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
from random import randint
import math
from networkx.algorithms import approximation as approx
from networkx.algorithms import traversal as tr
from networkx.algorithms import tree as tree
from networkx.drawing.nx_agraph import graphviz_layout
from graph_generation import generate_graph
from tree_generation import generate_tree
from scheduling_generation import scheduling
from hierarchy_pos import hierarchy_pos
import configparser
import time
config = configparser.ConfigParser()
config.read('config.yml', encoding='utf-8-sig')

G = nx.Graph()
H = nx.DiGraph()
distance = {}
best_nodes = {}

power_level = [int(e) for e in config['DEFAULT']
               ['niveles_de_potencia'].split(',')]
nodes = 0
max_nodes = int(config['DEFAULT']['max_nodes'])
root = int(config['DEFAULT']['root'])
n_ch = int(config['DEFAULT']['cantidad_canales'])

plt.gca().invert_yaxis()
position = ""

'''
ESTA ES LA EXPLICACION DEL ALGORITMO DE REUTILIZACION DE CANALES

Se convierte el grafo en un arbol, donde la cantidad de hijos de 
cada nodo son los nodos existentes en el primer nivel de conexion que tenga el nodo.
Luego, se recorre dicho arbol en BFS y se reserva un timeslot por cada nodo
hijo en el orden del BFS.

'''

# Asignando grafo al que sera el nuevo arbol
G = generate_graph(G, max_nodes, distance, power_level, nodes)

start = time.time()
generate_tree(H, G, root)
end = time.time()
print "Tiempo Generacion Abol"
print(end-start)
print "BFS"
bfs = list(nx.bfs_edges(H, root))

start = time.time()
sche = scheduling(H, root, bfs, n_ch)
end = time.time()
print "MATRIZ"
max = 0
for i in range(len(sche)):
    if len(sche[i]) > max:
        max = len(sche[i])
to_csv = []
first_row = []
for i in range(0,max):
    # first_row.append(i)
    first_row.insert(len(first_row), i)
first_row.insert(0, "Channel/Timeslot")
to_csv.append(first_row)
for i in range(len(sche)):
    print sche[i]
    to_csv_temp = []
    for tup in sche[i]:
        to_csv_temp.append(str(tup))
    to_csv_temp.insert(0,"Canal: "+ str(i))
    to_csv.append(to_csv_temp)
import csv
scheduling_file = open('scheduling_result.csv', 'w')
with scheduling_file:
   writer = csv.writer(scheduling_file, delimiter=',')
   writer.writerows(to_csv)
# max = 0
# for i in range(len(sche)):
#     if len(sche[i]) > max:
#         max = len(sche[i])
# for i in range(len(sche)):
#     if len(sche[i]) < max:
#         for i in range(abs(len(sche[i])-max)-1):
#             sche[i].append((None,None))
	# import pandas
	# df = pandas.DataFrame(sche)
	# print df


print "Tiempo Generacion Scheduling"
print(end-start)

plt.show()
pos = hierarchy_pos(H, root)
nx.draw(H, pos=pos, with_labels=True)
plt.draw()
plt.savefig(str(config['DEFAULT']['arbol']))
plt.show()
