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

G = nx.Graph()

distance = {}
best_nodes = {}
power_level = [15, 25, 55, 75]
nodes = 0
max_nodes = 10

plt.gca().invert_yaxis()
position = ""

def add_graphical_edge(G, i,k , peso):
	G.add_edge(i, k, weight=peso)
	G.add_edge(k, i)
	plt.clf()
	position = nx.get_node_attributes(G, 'pos')
	nx.draw(G,position,arrows=True)
	labels = nx.get_edge_attributes(G, 'weight')
	nx.draw_networkx_edge_labels(G, position, edge_labels=labels)
	nx.draw_networkx_labels(G, position, labels=None)
	plt.draw()	

# Permite encontrar nodos no vecinos
def non_neighbors_nodes(G,root):
	edges = tr.bfs_edges(G,root)
	item = [root] + [v for u, v in edges]
	print item
	for i in item:
		print "nodo ", i, " = ",list(nx.non_neighbors(G,i))

for i in range(0,max_nodes):
	if nodes < max_nodes:
		G.add_node(nodes, pos=(randint(0, 200), randint(0, 200) ))
		nodes = nodes + 1
		position = nx.get_node_attributes(G, 'pos')
		nx.draw(G,position,with_labels=True)
		plt.figure(1)
		plt.draw()


for i in range(0, len(G)):
	for j in range(0, len(G)):
		node_dist = math.hypot(G.node[j]['pos'][0] - G.node[i]['pos'][0], G.node[j]['pos'][1] - G.node[i]['pos'][1])
		node_dist = round(node_dist,1)
		node_dist = (j,node_dist)
		distance.setdefault(i, [])
		distance[i].append(node_dist)
		distance[i].sort(key=lambda tup: tup[1])
		if j == len(G)-1:
			print "**************************************"	
			print "REVISANDO NODO " + str(i)
			for k in range(0, len(distance[i])): 
				print " con nodo "+str(distance[i][k][0])+ " y peso "+str(distance[i][k][1])
				if i != k:
					peso = distance[i][k][1]
					if peso > 0 and peso <= power_level[0]:
						add_graphical_edge(G,i,distance[i][k][0],power_level[0])					
					if peso > power_level[0] and peso <= power_level[1]:	
						add_graphical_edge(G,i,distance[i][k][0],power_level[1])
					if peso > power_level[1] and peso <= power_level[2]:	
						add_graphical_edge(G,i,distance[i][k][0],power_level[2])	
					if peso > power_level[2] and peso <= power_level[3]:
						add_graphical_edge(G,i,distance[i][k][0],power_level[3])																	
	print distance[i]
	distance = {}		

non_neighbors_nodes(G,5)
position = nx.get_node_attributes(G, 'pos')
plt.gca().invert_yaxis()
nx.draw_networkx_labels(G, position, labels=None)
plt.draw()
plt.savefig("iot.png")
plt.show()
