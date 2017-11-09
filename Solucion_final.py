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

G = nx.Graph()

distance = {}
best_nodes = {}
power_level = [15, 25, 55, 75]
nodes = 0
max_nodes = 10

plt.gca().invert_yaxis()
position = ""


'''
ESTA ES LA EXPLICACION DEL ALGORITMO DE REUTILIZACION DE CANALES

Se convierte el grafo en un arbol, donde la cantidad de hijos de 
cada nodo son los nodos existentes en el primer nivel de conexion que tenga el nodo.
Luego, se recorre dicho arbol en BFS y se reserva un timeslot por cada nodo
hijo en el orden del BFS.

'''
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
	result = {}
	print item
	for i in item:
		print "nodo ", i, " = ",list(nx.non_neighbors(G,i))
		result[i] = list(nx.non_neighbors(G,i))
	return (item,result)

def calculate_matrix(bfs,non_neighbors):
	the_matrix = [None] * 4
	for i in range(0,4):
		the_matrix[i]= []
	matrix_index = 0
	matrix_position = 0
	for i in range(0,len(bfs)):
		neighbors = list(set(bfs)-set(non_neighbors[bfs[i]]))
		print neighbors
		for j in range(0,len(neighbors)):
			if bfs[i] == neighbors[j]:
				continue
			if matrix_index < 4:
				the_matrix[matrix_index].append( (str(bfs[i]) + '->' + str(neighbors[j]), (str(matrix_position))+' in '+ str(matrix_index) ))
				matrix_position += 1
			else:
				matrix_index = 0
			matrix_index += 1
		
	print the_matrix


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

result = non_neighbors_nodes(G, 5)
calculate_matrix(result[0], result[1])
position = nx.get_node_attributes(G, 'pos')
plt.gca().invert_yaxis()
nx.draw_networkx_labels(G, position, labels=None)
plt.draw()
plt.savefig("iot.png")
# Asignando grafo al que sera el nuevo arbol

H = nx.DiGraph()


def create_tree(H,G,root):
	print "CREANDO ARBOL"
	print sorted(G[root])
	H.add_node(root)
	first_iteration = True
	compare_list = [root]
	edges = tr.bfs_edges(G, root)
	item = [root] + [v for u, v in edges]
	while len(H.nodes()) < len(item):
		if first_iteration:
			print "In first level"
			for key, value in sorted(G[root].iteritems(), key=lambda (k, v): (v, k)):
				H.add_node(key)
				H.add_edge(root,key)
				compare_list.append(key)
				print "%s: %s" % (key, value)
			print len(compare_list)
			first_iteration = False
		else:
			print "In other level"
			print len(compare_list)
			for i in range(0,len(compare_list)):
				print G[i]
				for child_key, child_value in sorted(G[compare_list[i]].iteritems(), key=lambda (k, v): (v, k)):
					if child_key not in compare_list:
						H.add_node(child_key)
						H.add_edge(compare_list[i], child_key)
						compare_list.append(child_key)
						print "%s: %s" % (child_key, child_value)
		# count += 1
	print tree.is_tree(H)
	print "Terminando arbol"

create_tree(H,G,5)

plt.show()

# nx.write_dot(H, 'test.dot')
# plt.title('draw_networkx')
# pos = nx.graphviz_layout(H, prog='dot')
# nx.draw(H, pos, with_labels=False, arrows=False)
# plt.savefig('nx_test.png')

nx.draw(H, pos=graphviz_layout(H), node_size=1600, cmap=plt.cm.Blues,
        node_color=range(len(H)),
        prog='dot')
plt.show()
